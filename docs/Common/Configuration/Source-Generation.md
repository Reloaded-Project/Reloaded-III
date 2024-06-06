!!! tip "A standalone tool will be provided to generate C# or Rust code directly from the [config.toml][config-schema] schema file."

In order to keep the [`config.toml`][config-schema] schema file in sync with the source code,
a standalone tool will be provided to automate the code generation process for a given language.

This will allow for adding config capabilities to new programming languages without the need for
the language to support source generation natively.

### Example Usage

!!! tip "It's a basic CLI tool 😉"


```bash
config-codegen --lang csharp --input config.toml --output MyModConfig.cs
```

or

```bash
config-codegen --lang rust --input config.toml --output my_mod_config.rs
```

That said, you'll never actually need to run it manually. We'll try to integrate it to build process
wherever possible.

### Integration with Build Systems

!!! info "Examples of how we can integrate with build system."

=== "Rust"

    In a Rust project using Cargo, we can add a build script that runs the code generation tool directly:

    ```toml
    [build-dependencies]
    config-codegen = "1.0"
    ```

    ```rust
    // build.rs
    fn main() {
        config_codegen::generate("config.toml", "src/my_mod_config.rs");
    }
    ```

    Since the original code is Rust, we can use it as a regular library.

=== "C#"

    For other languages like C#, this can be done with something like:

    1. Create a NuGet Package that wraps the Rust Code Gen Binary.

          - Include the compiled Rust library binaries for different platforms.
          - Include a `.targets` file to run the tool.
              - This will allow code to be executed during build.
          - Publish as NuGet package.

    The `.targets` file may look something like:

    ```xml
    <Project>
    <!-- Not Tested, But it's Something like This -->
    <Target Name="GenerateMyModConfig" BeforeTargets="BeforeBuild">
        <PropertyGroup>
            <R3ConfigCodeGenerator Condition="$([MSBuild]::IsOsPlatform('Windows')) And $([System.Runtime.InteropServices.RuntimeInformation]::OSArchitecture.X86)">$(MSBuildThisFileDirectory)../../tools/win-x86/my_mod_config_codegen.exe</R3ConfigCodeGenerator>
            <R3ConfigCodeGenerator Condition="$([MSBuild]::IsOsPlatform('Windows')) And $([System.Runtime.InteropServices.RuntimeInformation]::OSArchitecture.X64)">$(MSBuildThisFileDirectory)../../tools/win-x64/my_mod_config_codegen.exe</R3ConfigCodeGenerator>
            <R3ConfigCodeGenerator Condition="$([MSBuild]::IsOsPlatform('Linux')) And $([System.Runtime.InteropServices.RuntimeInformation]::OSArchitecture.X86)">$(MSBuildThisFileDirectory)../../tools/linux-x86/my_mod_config_codegen</R3ConfigCodeGenerator>
            <R3ConfigCodeGenerator Condition="$([MSBuild]::IsOsPlatform('Linux')) And $([System.Runtime.InteropServices.RuntimeInformation]::OSArchitecture.X64)">$(MSBuildThisFileDirectory)../../tools/linux-x64/my_mod_config_codegen</R3ConfigCodeGenerator>
            <R3ConfigCodeGenerator Condition="$([MSBuild]::IsOsPlatform('Linux')) And $([System.Runtime.InteropServices.RuntimeInformation]::OSArchitecture.Arm64)">$(MSBuildThisFileDirectory)../../tools/linux-arm64/my_mod_config_codegen</R3ConfigCodeGenerator>
            <R3ConfigCodeGenerator Condition="$([MSBuild]::IsOsPlatform('OSX')) And $([System.Runtime.InteropServices.RuntimeInformation]::OSArchitecture.X64)">$(MSBuildThisFileDirectory)../../tools/osx-x64/my_mod_config_codegen</R3ConfigCodeGenerator>
            <R3ConfigCodeGenerator Condition="$([MSBuild]::IsOsPlatform('OSX')) And $([System.Runtime.InteropServices.RuntimeInformation]::OSArchitecture.Arm64)">$(MSBuildThisFileDirectory)../../tools/osx-arm64/my_mod_config_codegen</R3ConfigCodeGenerator>
        </PropertyGroup>
        <Exec Condition="$([MSBuild]::IsOsPlatform('Linux')) Or $([MSBuild]::IsOsPlatform('OSX'))" Command="chmod +x $(R3ConfigCodeGenerator)" />
        <Exec Command="$(R3ConfigCodeGenerator) --input config.toml --output MyModConfig.cs" />
    </Target>
    </Project>
    ```

    Then to use the generator, simply add the NuGet to the project's `.csproj` file:

    ```xml
    <ItemGroup>
        <PackageReference Include="Reloaded3Config.CodeGeneration" Version="1.0.0" />
    </ItemGroup>
    ```

### Generated Code Structure

!!! info "This is an example of generated code"

The generated code includes:

- A struct for the root config object, based on [`[general]`][config-schema-general] section.
- Nested structs for each config group.
- Properties for each setting, with appropriate types and defaults.
  - The types are based on the [`min`][config-schema-min] and [`max`][config-schema-max] values,
    falling back to the smallest possible type.
  - Enums are generated for [`Choice`][config-schema-choice] settings.
- Getters to access setting values.

Example TOML:

```toml
[general]
name = "My Mod"
author = "John Doe"
language_folder = "config"
default_language = "en-GB.toml"

[[settings]]
index = 0
type = "bool"
name = "ENABLE_FEATURE"
description = "Enable the special feature"
default = false
apply_on = "save"

[[settings]]
index = 1
type = "int"
name = "MAX_COUNT"
description = "Maximum count for the feature"
default = 10
min = 1
max = 100
apply_on = "restart"

[[settings]]
index = 2
type = "choice"
name = "DIFFICULTY"
description = "Game difficulty"
choices = ["EASY", "NORMAL", "HARD"]
default = "NORMAL"

[[settings]]
index = 3
type = "color"
name = "UI_COLOR"
description = "UI accent color"
default = "#FF0000"
alpha = true

[group]
name = "Advanced"
description = "Advanced settings"

[[settings]]
index = 4
type = "string_list"
name = "BLACKLISTED_MODS"
description = "List of blacklisted mods"
default = []
```

!!! note "SettingsSource API"

    === "C#"

        ```csharp
        public interface ISettingsSource
        {
            bool GetBool(int index, bool defaultValue);
            int GetInt(int index, int defaultValue);
            string GetString(int index, string defaultValue);
            string[] GetStringList(int index, string[] defaultValue);
            Color GetColor(int index, Color defaultValue);
            T GetEnum<T>(int index, T defaultValue) where T : Enum;

            void SubscribeBool(int index, Action<bool> callback);
            void SubscribeInt(int index, Action<int> callback);
            void SubscribeString(int index, Action<string> callback);
            void SubscribeStringList(int index, Action<string[]> callback);
            void SubscribeColor(int index, Action<Color> callback);
            void SubscribeEnum<T>(int index, Action<T> callback) where T : Enum;
        }
        ```

    === "Rust"

        ```rust
        pub trait SettingsSource {
            fn get_bool(&self, index: u32, default: bool) -> bool;
            fn get_int(&self, index: u32, default: i32) -> i32;
            fn get_string(&self, index: u32, default: &str) -> String;
            fn get_string_list(&self, index: u32, default: &[String]) -> Vec<String>;
            fn get_color(&self, index: u32, default: Color) -> Color;
            fn get_enum<T: FromPrimitive + Copy>(&self, index: u32, default: T) -> T;

            fn subscribe_bool(&mut self, index: u32, callback: fn(bool));
            fn subscribe_int(&mut self, index: u32, callback: fn(i32));
            fn subscribe_string(&mut self, index: u32, callback: fn(String));
            fn subscribe_string_list(&mut self, index: u32, callback: fn(Vec<String>));
            fn subscribe_color(&mut self, index: u32, callback: fn(Color));
            fn subscribe_enum<T: FromPrimitive + Copy>(&mut self, index: u32, callback: fn(T));
        }
        ```

=== "C#"

    ```csharp
    public struct MyModConfig
    {
        private bool _enableFeature;
        private byte _maxCount;
        private Difficulty _difficulty;
        private Color _uiColor;
        private AdvancedSettings _advanced;

        public bool EnableFeature => _enableFeature;
        public byte MaxCount => _maxCount;
        public Difficulty Difficulty => _difficulty;
        public Color UiColor => _uiColor;
        public AdvancedSettings Advanced => _advanced;

        public delegate void EnableFeatureChangedHandler(bool value);

        public MyModConfig(ISettingsSource source, EnableFeatureChangedHandler onEnableFeatureChanged)
        {
            _enableFeature = source.GetBool(0, false);
            _maxCount = (byte)source.GetInt(1, 10);
            _difficulty = source.GetEnum<Difficulty>(2, Difficulty.Normal);
            _uiColor = source.GetColor(3, new Color(255, 0, 0, 255));
            _advanced.Initialize(source);

            // Ensure that the initial value is set before subscribing to changes
            source.SubscribeBool(0, newValue => {
                _enableFeature = newValue;
                onEnableFeatureChanged(newValue);
            });
        }

        public struct AdvancedSettings
        {
            private string[] _blacklistedMods;
            public string[] BlacklistedMods => _blacklistedMods;

            public AdvancedSettings(ISettingsSource source)
            {
                _blacklistedMods = source.GetStringList(4, Array.Empty<string>());
            }
        }
    }

    public enum Difficulty
    {
        Easy,
        Normal,
        Hard
    }
    ```

=== "Rust"

    ```rust
    pub struct MyModConfig {
        enable_feature: bool,
        max_count: u8,
        difficulty: Difficulty,
        ui_color: Color,
        advanced: AdvancedSettings,
    }

    impl MyModConfig {
        pub type EnableFeatureChangedHandler = fn(bool);

        pub fn new(source: &mut dyn SettingsSource, on_enable_feature_changed: EnableFeatureChangedHandler) -> Self {
            let result = Self {
                enable_feature: source.get_bool(0, false),
                max_count: source.get_int(1, 10) as u8,
                difficulty: source.get_enum(2, Difficulty::Normal),
                ui_color: source.get_color(3, Color::new(255, 0, 0, 255)),
                advanced: AdvancedSettings::new(source),
            }

            // Subscribe to changes after initializing the values
            source.subscribe_bool(0, move |new_value| {
                config.enable_feature = new_value;
                on_enable_feature_changed(new_value);
            });

            result
        }

        pub fn enable_feature(&self) -> bool {
            self.enable_feature
        }

        pub fn max_count(&self) -> u8 {
            self.max_count
        }

        pub fn difficulty(&self) -> Difficulty {
            self.difficulty
        }

        pub fn ui_color(&self) -> Color {
            self.ui_color
        }

        pub fn advanced(&self) -> &AdvancedSettings {
            &self.advanced
        }
    }

    pub struct AdvancedSettings {
        blacklisted_mods: Vec<String>,
    }

    impl AdvancedSettings {
        pub fn new(source: &mut dyn SettingsSource) -> Self {
            Self {
                blacklisted_mods: source.get_string_list(4),
            }
        }

        pub fn blacklisted_mods(&self) -> &[String] {
            &self.blacklisted_mods
        }
    }

    #[derive(Clone, Copy, PartialEq, Eq)]
    pub enum Difficulty {
        Easy,
        Normal,
        Hard,
    }
    ```

!!! note "In the generated code, the types are inferred based on the [`min`][config-schema-min] and [`max`][config-schema-max] values."

    The actual values use the smallest possible type that can represent the range.

!!! note "Enums are auto generated for [`Choice`][config-schema-choice] settings."

!!! note "The generated code contains the defaults for the settings."

    This allows you for migration of settings created in older versions.

!!! note "The callback functions are only defined for settings where [`apply_on`][config-schema-general] is not set to `restart`"

    For settings with [`apply_on`][config-schema-general] set to `restart`, the changes will only
    take effect after a restart, so there's no need to handle them in real-time.

    These callbacks are specified in the constructor, to ensure at compile time the user includes
    a handler where necessary.

    The callbacks are added in index order to make migrations between versions easier.

[config-schema]: ./Config-Schema.md
[config-schema-general]: ./Config-Schema.md#general-metadata
[config-schema-min]: ./Config-Schema.md#integer-setting
[config-schema-max]: ./Config-Schema.md#integer-setting
[config-schema-choice]: ./Config-Schema.md#choice-enum-setting