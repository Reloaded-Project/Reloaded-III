!!! info "This attempts to demystify some parts of `allocator_api` in Rust"

The use of custom allocators is not common in Rust. When I started trying to use them,
I got stuck with many questions.

Blog posts, GitHub Issue reading, Discord Rust Community server, not much.
There was a small gap in knowledge there for someone who was a bit newer to Rust.

!!! note "There are two ways to use an allocator."

    By dynamic dispatch (dyn trait) and static dispatch.<br/>
    This page will focus on the latter.

## How do I Pass Allocator to a Function?

!!! info "There are two ways to pass an allocator to a function."

The first way is for zero-sized allocators that implement `Clone`, like the `System` allocator.

```rust
// Using system allocator
use std::alloc::System;
let t2 = Tessellator::new_in(System);
```

!!! tip "In this case, the zero sized struct is eliminated by the compiler"

    And calls to `Clone` are turned into no-op.

The other way is passing an allocator by reference; which looks something like this:

```rust
// Create and use a new bump arena (e.g. bumpalo)
let bump = Bump::new();
let mut v = Vec::new_in(&bump);
```

### How does `&Allocator` magically work?

!!! info "What magic allows you to pass both a value and a reference via the same function?"

It's very easy to get confused here, I certainly did.

The magic lies in the following Rust default trait implementation:

```rust
// This implementation is provided by the standard library
unsafe impl<A> Allocator for &A
where
    A: Allocator + ?Sized,
{
    fn allocate(&self, layout: Layout) -> Result<NonNull<[u8]>, AllocError> {
        (**self).allocate(layout)
    }

    unsafe fn deallocate(&self, ptr: NonNull<u8>, layout: Layout) {
        (**self).deallocate(ptr, layout)
    }

    // Other methods are implemented similarly...
}
```

!!! tip "This blanket implementation implements `Allocator` for `&Allocator`."

Therefore, when you pass an `&Allocator` to a function, you are also passing an `Allocator`.
This is the magic behind the scene.

When you `Clone` an `&Allocator`, you simply clone reference itself (1 pointer),
as evident by this piece of `std`:

```rust
/// Shared references can be cloned, but mutable references *cannot*!
#[stable(feature = "rust1", since = "1.0.0")]
impl<T: ?Sized> Clone for &T {
    #[inline(always)]
    #[rustc_diagnostic_item = "noop_method_clone"]
    fn clone(&self) -> Self {
        *self
    }
}
```

!!! tip "Here `&self` is `&&T` since the trait is for `&T`."

And to make that work 'just right', the allocators use the [interior mutability] pattern:

```rust
#[derive(Debug)]
pub struct Bump {
    // The current chunk we are bump allocating within.
    current_chunk_footer: Cell<NonNull<ChunkFooter>>,
    allocation_limit: Cell<Option<usize>>, // <= See? Cell right there!
}
```

## Using the Allocator Multiple Times in a Method

!!! info "You can use an allocator multiple times in a method with `Clone` trait bound."

    i.e. `Allocator + Clone`

```rust
// Struct with multiple Vecs using the same allocator
struct MultiVecStruct<A: Allocator + Clone> {
    data1: Vec<i32, A>,
    data2: Vec<String, A>,
    data3: Vec<bool, A>,
}

impl<A: Allocator + Clone> MultiVecStruct<A> {
    // Constructor that uses the allocator multiple times
    fn new_in(allocator: A) -> Self {
        Self {
            data1: Vec::new_in(allocator.clone()),
            data2: Vec::new_in(allocator.clone()),
            data3: Vec::new_in(allocator),
        }
    }
}

fn main() {
    // Create an instance of MultiVecStruct
    let mut multi_vec = MultiVecStruct::new_in(MyAllocator);
    // ...
}
```

!!! question "Wouldn't `cloning` an allocator create more allocators?"

    Surprisingly, no. For the finite details, see [How does &Allocator magically work?](#how-does-allocator-magically-work).


## Does `&Allocator` Increase Struct Size?

!!! info "It depends."

To give an example:

```rust
Box<u8, System> // 8 bytes (64-bit)
```

And if you use an *allocator by reference*:

```rust
Box<u8, &System> // 16 bytes (64-bit)
```

So yes, the struct size itself increases.

***However***, the impact of this depends on the semantics of the code.

If the type (i.e. `Box<u8, &System>`) is stored *on the stack* (not heap), then there should
actually be no difference provided LLVM correctly optimizes the program.

This is because the *value is copied and then never used*, so LLVM will no-op that out.

[Godbolt Example] with `-C opt-level=3`

```rust
#![feature(allocator_api)]
use std::alloc::System;

#[no_mangle]
pub fn create_box_with_system_ref<'a>() -> *mut u8 {
    let mut bx: Box<u8, &System> = Box::new_in(42, &System);
    bx.as_mut() as *mut u8
}

#[no_mangle]
pub fn create_box_with_system() -> *mut u8 {
    let mut bx: Box<u8, System> = Box::new_in(42, System);
    bx.as_mut() as *mut u8
}
```

Creates basically identical assembly for both functions:

```asm
create_box_with_system_ref:
        push    rbx
        mov     edi, 1
        call    qword ptr [rip + malloc@GOTPCREL]
        test    rax, rax
        je      .LBB0_2
        mov     rdi, rax
        mov     rbx, rax
        call    qword ptr [rip + free@GOTPCREL]
        mov     rax, rbx
        pop     rbx
        ret
.LBB0_2:
        mov     edi, 1
        mov     esi, 1
        call    qword ptr [rip + alloc::alloc::handle_alloc_error::h38a274d2e3660aa0@GOTPCREL]

create_box_with_system:
        push    rbx
        mov     edi, 1
        call    qword ptr [rip + malloc@GOTPCREL]
        test    rax, rax
        je      .LBB1_2
        mov     rdi, rax
        mov     rbx, rax
        call    qword ptr [rip + free@GOTPCREL]
        mov     rax, rbx
        pop     rbx
        ret
.LBB1_2:
        mov     edi, 1
        mov     esi, 1
        call    qword ptr [rip + alloc::alloc::handle_alloc_error::h38a274d2e3660aa0@GOTPCREL]
```

!!! warning "Please ignore the fact this is improper, flawed code."

    This example is just supposed to illustrate that the generated code is identical,
    even in the presence of calling `malloc` (Allocate) and `free` (Drop).

In other words, providing a custom allocator for short lived stack allocations is perfect.

[interior mutability]: https://doc.rust-lang.org/book/ch15-05-interior-mutability.html
[Godbolt Example]: https://godbolt.org/z/jfWGfd1Mj