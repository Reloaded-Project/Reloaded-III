!!! info "This page contains miscellaneous notes on scaling multiplayer mods to a large number of clients."

    Specifically aiming at bandwidth saving.

    The aim is 63 clients with an upload bandwidth less than 50Mbps for simple racing games.

<!-- TODO: Move this to relevant mod(s) -->

This page hosts the less commonly known strategies and background knowledge for optimizing
networking for multiplayer game mods.

This focuses mainly on regular `tick` frames, rather than event messages.

## Using ZStd in Block Mode

!!! info "Standard ZStd files have some undesireable metadata"

For example:

- Magic Number (4 bytes)
- Frame Header (2-14 bytes)
- Checksum (0-4 bytes)

When trying to save every byte, reclaiming those 10 or so bytes is worthwhile.

To do this, we can compress individual *zstandard blocks*, as opposed to relying on the high level API.

```
ZSTD_getBlockSize
ZSTD_compressBlock
ZSTD_decompressBlock
ZSTD_insertBlock
```

Namely, we can block the data up ourselves.
For example, packed floats could be one block, while the rest of the data could be another block.

### Use a Dictionary

!!! info "We can pre-generate dictionaries for various sections of data."

For each version of a multiplayer mod we may have pre-trained dictionaries for each type of data.

For example, a dictionary for the floats in the format described at [Float Compression].

This in turn improves huffman utilization and dictionary efficiency.

### Shorten Block Header

!!! info "Since we're dealing with shorter packets, we can shorten the block header."

By default the ZSTD block header has the following data structure:

```c
typedef struct {
  int Last_Block : 1;
  int Block_Type : 2;
  int Block_Size : 21;
} Block_Header;
```

This uses 3 bytes. We can shorten it to 2 bytes with the following structure.

```c
typedef struct {
  int Last_Block : 1;
  int Block_Type : 2;
  int Block_Size : 13;
} Block_Header_New;
```

This gives us a max block size of 8192 bytes.
A packet that can handle roughly 255-ish players in a previous mod of mine.

## Float Compression

!!! info "We can transform/rearrange the sent data structure to improve bandwidth usage."

!!! tip "There is a fantastic [blog post by Aras Pranckevičius][float-compression-filters] covering this, and more"

    You can consider this a summary of that article.

For this example, suppose we have a simplified player structure:

```rust
f32 x;
f32 y;
f32 z;
f32 vel; // Velocity
```

Imagine we're dealing with a 63 player lobby, just sending these 4
floats alone would be `63 * 16 = 1008 bytes`. We can improve this.

### Structure of Arrays

Instead of sending player structures one by one:

```
x0, y0, z0, vel0, x1, y1, z1, vel1, ...
```

We can choose to rearrange the data in the following manner:

```
x0, x1, y0, y1, z0, z1, vel0, vel1, ...
```

This increases the likelihood of repeated data.

Many players may for example be traversing on the same straight line;
meaning the first 1/2 bytes of the floats may match.

### Reorder Bytes

!!! info "Remember how I said `the first 1/2 bytes of the floats may match`?"

    Well, compressors like zstd, zlib etc. are only good at saving space when there
    are matches of at least 3 bytes.

It is possible to further rearrange the data such that the matching bytes
are grouped together. Consider the following:

```
(x0[0], x1[0]), (x0[1], x1[1]), (x0[2], x1[2]), (x0[3], x1[3]), (y0[0], y1[0]), (y0[1], y1[1]) ...
```

Now we've put the first bytes of each float together.

As the first bytes are likely to repeat across values, our compression ratio increases.

### Delta Encoding

!!! tip "With some trickery you can rearrange floats to improve the probability of repeated `00` sequences"

    This slightly improves compression ratio.

Consider two cars pushing against each other on a straight line, meaning
one of their positions only varies slightly in an axis:

- x0 = `1327.784` = `44 A5 F9 18`
- x1 = `1320.432` = `44 A5 0D D4`

When reordered using the previous approach we get:

```
(x0[0], x1[0]), (x0[1], x1[1]), (x0[2], x1[2]), (x0[3], x1[3])
```

which is

```
(44 44) (A5 A5) (F9 0D) (18 D4)
```

We have repeating bytes here which is handy, however note that these bytes repeat; with delta encoding
the start can actually just be:

```
(00 00) (00 00)
```

Which is calculated by subtracting current byte from previous byte, i.e.

- x0[0] = x0[0] - 0
- x1[0] = x1[0] - x0[0]
- ... etc.

The longer sequence of bytes will improve efficiency of compression.
Particularly for compressors using huffman coding.

#### Delta Encoding Pseudocode

```rust
pub fn encode_delta_dif(data: &mut [u8]) {
    let mut prev: u8 = 0;
    for byte in data.iter_mut() {
        let v = *byte;
        *byte = v.wrapping_sub(prev);
        prev = v;
    }
}

pub fn decode_delta_dif(data: &mut [u8]) {
    let mut prev: u8 = 0;
    for byte in data.iter_mut() {
        let v = *byte;
        let decoded = prev.wrapping_add(v);
        *byte = decoded;
        prev = decoded;
    }
}
```

Additional optimizations are possible for longer sequences.

However for a typical 16 player lobby we expect 15 bytes; for most cases SIMD's out the question.

## Distance-Based Rate Reduction

!!! tip "You can reduce bandwidth usage by using distance-based rate reduction method."

This involves sending updates to players at different rates depending on their distance
from the current player. This is achieved using a modulo operation on the game's update tick.

### 1. Distance Calculation

Calculate the distance between the other player and current player.
To calculate the distance between 2 3D vectors, use the [Euclidean distance formula][Euclidiean distance formula].

```rust
fn calculate_distance(player1: &Player, player2: &Player) -> f32 {
    let dx = player1.x - player2.x;
    let dy = player1.y - player2.y;
    let dz = player1.z - player2.z;
    (dx * dx + dy * dy + dz * dz).sqrt()
}
```

### 2. Determine Frequency

!!! info "Every time you're about to construct a packet to send, check if it should be sent based on distance."

```rust
fn should_send_update(tick: i32, distance: f32) -> bool {
    if distance <= 100.0 {
        return true; // Send every tick
    }
    if distance <= 200.0 {
        return tick % 2 == 0; // Send every 2nd tick
    } else {
        return tick % 4 == 0; // Send every 4th tick
    }
}
```

Limit the min frequency to 1/4th of the tick rate (or base frequency).
For the technical reason, see [Traffic Bursting](#traffic-bursting).

### Considerations

1. **Interpolation**: Clients may need to interpolate between less frequent updates for smooth gameplay.
    - Include info such as `steer amount` and `throttle pressure` in the update packet.
    - And replay those (if required by game code) in the next game tick if we don't receive an update in time.

### Traffic Bursting

!!! question "But why does the above work?"

    Every 4th tick, we send an update to all players, ***would this not be throttled?***

    We don't want to drop/delay packets that exceed max transfer late.

Surprisingly, no. ISP infrastructure commonly has mechanisms to handle very short bursts in traffic.

The magic lies in RFC 2697 and the commonly used [token bucket algorithm][token bucket algorithm].

#### Token Bucket Algorithm

!!! info "The `token bucket` algorithm is commonly used to control the rate of data transmission on networks."

1. Imagine a bucket that holds tokens.
2. Tokens are added to the bucket at a constant rate (the `fill rate`).
3. When data needs to be sent, it must collect a token from the bucket.
4. If the bucket is empty, the data must wait.
5. The bucket has a maximum capacity; once full, new tokens are discarded.

***This algorithm allows for bursts of data (up to the bucket's capacity)*** while maintaining a
long-term average rate.

An example:

| Tick | Action         | Tokens Added | Tokens Used | Available Tokens |
| ---- | -------------- | ------------ | ----------- | ---------------- |
| 0    | Start          | 0            | 0           | 300.00           |
| 1    | Send to all    | 131.25       | 300         | 131.25           |
| 2    | Send to nearby | 131.25       | 75          | 187.50           |
| 3    | Send to nearby | 131.25       | 75          | 243.75           |
| 4    | Send to nearby | 131.25       | 75          | 300.00           |
| 5    | Send to all    | 131.25       | 300         | 131.25           |
| 6    | Send to nearby | 131.25       | 75          | 187.50           |
| 7    | Send to nearby | 131.25       | 75          | 243.75           |
| 8    | Send to nearby | 131.25       | 75          | 300.00           |
| 9    | Send to all    | 131.25       | 300         | 131.25           |
| 10   | Send to nearby | 131.25       | 75          | 187.50           |
| 11   | Send to nearby | 131.25       | 75          | 243.75           |
| 12   | Send to nearby | 131.25       | 75          | 300.00           |

While we're sending what isn't the 4th tick, the bucket slowly fills (`131.25` -> `243.75`), as our
transfer rate is lower than the fill rate.

When we send the `big` update every 4th tick (greater than `fill rate`), we simply use up all the
excess tokens from the bucket that we gained in the remaining 3 ticks. This brings us back to `131.25`.

!!! tip "In practice, for a stable experience, the `Tokens Added` (fill rate) should be greater than the `Tokens Used` over 4 ticks."

    This lets us use [Excess Burst Size (EBS)](#excess-burst-size-ebs) to accomodate any one off events.
    that are not sent at a regular interval.

#### Excess Burst Size (EBS)

!!! info "Sometimes we may need to accomodate small spikes in traffic."

    What if:

    - Someone opens a web page while you're gaming?
    - You need some one off events (e.g. `lap count incremented`)

    Or anything else outside of the regular tick rate?

While our current token bucket implementation shows how we can handle regular traffic patterns,
you might have noticed that the available tokens are gradually depleting over time.

In real-world scenarios, we sometimes need to accommodate larger spikes in traffic.
This is where the Excess Burst Size (EBS) comes into play.

!!! tip "Excess Burst Size (EBS) is an additional allowance of tokens that can be borrowed when the regular token bucket"

1. When the regular token bucket is empty, the system can borrow tokens from the EBS.
2. These borrowed tokens allow transmission of data even when the regular bucket is depleted.
3. The borrowed tokens are then repaid over time as the regular bucket refills.

#### Example with EBS

Let's modify our previous example to include EBS.

We'll set the EBS to 300 tokens. This means available tokens can go up to `-300`, provided
that at the end of a given `time slice`, they are reset to 0.

| Tick | Action                | Tokens Added | Tokens Used | Available Tokens |
| ---- | --------------------- | ------------ | ----------- | ---------------- |
| 0    | Start                 | 0            | 0           | 100              |
| 1    | Send to nearby        | 150          | 75          | 175              |
| 2    | Send to nearby        | 150          | 75          | 250              |
| 3    | Send to nearby        | 150          | 75          | 325              |
| 4    | Send to all           | 150          | 300         | 175              |
| 5    | ***SEND HUGE EVENT*** | 150          | 400         | -100             |
| 6    | Send to nearby        | 150          | 75          | -25              |
| 7    | Send to nearby        | 150          | 75          | 50               |
| 8    | Send to nearby        | 150          | 75          | 125              |
| 9    | Send to all           | 150          | 300         | -25              |
| 10   | Send to nearby        | 150          | 75          | 50               |
| 11   | Send to nearby        | 150          | 75          | 125              |
| 12   | Send to nearby        | 150          | 75          | 200              |
| 13   | Send to all           | 150          | 300         | 50               |
| 14   | Send to nearby        | 150          | 75          | 125              |
| 15   | Send to nearby        | 150          | 75          | 200              |
| 16   | Send to nearby        | 150          | 75          | 275              |
| 17   | Send to all           | 150          | 300         | 125              |
| 18   | Send to nearby        | 150          | 75          | 200              |
| 19   | Send to nearby        | 150          | 75          | 275              |
| 20   | Send to nearby        | 150          | 75          | 350              |

In this example, we hit EBS at Tick 5, and have fully recovered it by tick 18.

If we have a rate of 100Hz, this means we recovered in 13 frames.

!!! note "This isn't exactly how it works 100%"

    But it's a good way to visualize it, and it's valid for our use case.

In practice, EBS is limited to a certain time slice.

!!! tip "The ratio of EBS to CBS (regular fill rate) is usually 2:1."

    This is why we limit the minimum frequency to 1/4th of the tick rate.

##### Extra Information

For additional information, ***ask an AI***, or Google it.

The magic lies in RFC 2697, the terms `CIR`, `CBS`, and `EBS` will be handy here.

In simple terms:

- ***CIR*** is what your upload bandwidth is advertised by your ISP. This determines `fill rate`.
- ***CBS*** is basically determines how much you are guaranteed to be able to burst.
- ***EBS*** is extra ontop of ***CBS*** but these packets may be dropped if there's congestion.

## Jitter Buffer

TODO: Revisit Tweakbox code and Document This.

[Euclidiean distance formula]: https://en.wikipedia.org/wiki/Euclidean_distance
[token bucket algorithm]: https://en.wikipedia.org/wiki/Token_bucket
[float-compression-filters]: https://aras-p.info/blog/2023/02/01/Float-Compression-3-Filters/
[Float Compression]: #float-compression