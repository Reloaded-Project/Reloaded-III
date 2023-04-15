---
hide:
  - toc
---

!!! warning

    Extreme work in progress. We've only gotten started!

## What is Reloaded III

!!! info

    Reloaded III is a placeholder name; we're open for suggestions.  

**[Reloaded III]** is a formal specification for an improved version of [Reloaded-II](https://reloaded-project.github.io/Reloaded-II/), a universal Game Modding framework.  

<div align="center">
	<img src="./Images/Reloaded3ConsoleLogo.png" width="550" align="center" />
	<br/><br/>
</div>

It is an ***extensible*** and ***modular*** framework that allows you to create your own mods for any game on virtually any platform.  

R3 is built on a tried and tested architecture; that ensures games stay functional post updates, and ***good*** support for new games can be added ***fast***.  

Don't waste time making a whole infrastructure for your game; *go mod stuff instead!*.  

!!! question
    
    So what is Reloaded about? 👇 Below are some goals of the project.  

## Mod Loader

<!-- Cards -->
<!-- 
	Icons: https://squidfunk.github.io/mkdocs-material/reference/icons-emojis/
	The dirty trick with images is we place them inline in text, let the page build
	and then copy the HTML out.

	I have no idea why MkDocs Material isn't properly handling icons in HTML out of the box.
-->

<!-- Portable & Modular -->
<div class="pillarwrapper">
    <div class="pillarcard">
		<p class="pillartitle">
			<span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M10.04 20.4H7.12c-.93 0-1.82-.4-2.48-1.04C4 18.7 3.6 17.81 3.6 16.88V7.12c0-.93.4-1.82 1.04-2.48C5.3 4 6.19 3.62 7.12 3.62h2.92V20.4M7.12 2A5.12 5.12 0 0 0 2 7.12v9.76C2 19.71 4.29 22 7.12 22h4.53V2H7.12M5.11 8c0 1.04.84 1.88 1.89 1.88 1.03 0 1.87-.84 1.87-1.88S8.03 6.12 7 6.12c-1.05 0-1.89.84-1.89 1.88m12.5 3c1.11 0 2.01.89 2.01 2 0 1.12-.9 2-2.01 2-1.11 0-2.03-.88-2.03-2 0-1.11.92-2 2.03-2m-.73 11A5.12 5.12 0 0 0 22 16.88V7.12C22 4.29 19.71 2 16.88 2h-3.23v20h3.23Z"></path></svg></span>
			<strong>Portable</strong>
		</p>
		<hr class="pillarseparator" />
        <p>
			Support a variety of platforms.<br/>
			Native x86, x64, Switch ARM, .NET 7+ etc.
		</p>
    </div>

	<div class="pillarcard">
		<p class="pillartitle">
			<span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M7.429 1.525a6.593 6.593 0 0 1 1.142 0c.036.003.108.036.137.146l.289 1.105c.147.56.55.967.997 1.189.174.086.341.183.501.29.417.278.97.423 1.53.27l1.102-.303c.11-.03.175.016.195.046.219.31.41.641.573.989.014.031.022.11-.059.19l-.815.806c-.411.406-.562.957-.53 1.456a4.588 4.588 0 0 1 0 .582c-.032.499.119 1.05.53 1.456l.815.806c.08.08.073.159.059.19a6.494 6.494 0 0 1-.573.99c-.02.029-.086.074-.195.045l-1.103-.303c-.559-.153-1.112-.008-1.529.27-.16.107-.327.204-.5.29-.449.222-.851.628-.998 1.189l-.289 1.105c-.029.11-.101.143-.137.146a6.613 6.613 0 0 1-1.142 0c-.036-.003-.108-.037-.137-.146l-.289-1.105c-.147-.56-.55-.967-.997-1.189a4.502 4.502 0 0 1-.501-.29c-.417-.278-.97-.423-1.53-.27l-1.102.303c-.11.03-.175-.016-.195-.046a6.492 6.492 0 0 1-.573-.989c-.014-.031-.022-.11.059-.19l.815-.806c.411-.406.562-.957.53-1.456a4.587 4.587 0 0 1 0-.582c.032-.499-.119-1.05-.53-1.456l-.815-.806c-.08-.08-.073-.159-.059-.19a6.44 6.44 0 0 1 .573-.99c.02-.029.086-.075.195-.045l1.103.303c.559.153 1.112.008 1.529-.27.16-.107.327-.204.5-.29.449-.222.851-.628.998-1.189l.289-1.105c.029-.11.101-.143.137-.146zM8 0c-.236 0-.47.01-.701.03-.743.065-1.29.615-1.458 1.261l-.29 1.106c-.017.066-.078.158-.211.224a5.994 5.994 0 0 0-.668.386c-.123.082-.233.09-.3.071L3.27 2.776c-.644-.177-1.392.02-1.82.63a7.977 7.977 0 0 0-.704 1.217c-.315.675-.111 1.422.363 1.891l.815.806c.05.048.098.147.088.294a6.084 6.084 0 0 0 0 .772c.01.147-.038.246-.088.294l-.815.806c-.474.469-.678 1.216-.363 1.891.2.428.436.835.704 1.218.428.609 1.176.806 1.82.63l1.103-.303c.066-.019.176-.011.299.071.213.143.436.272.668.386.133.066.194.158.212.224l.289 1.106c.169.646.715 1.196 1.458 1.26a8.094 8.094 0 0 0 1.402 0c.743-.064 1.29-.614 1.458-1.26l.29-1.106c.017-.066.078-.158.211-.224a5.98 5.98 0 0 0 .668-.386c.123-.082.233-.09.3-.071l1.102.302c.644.177 1.392-.02 1.82-.63.268-.382.505-.789.704-1.217.315-.675.111-1.422-.364-1.891l-.814-.806c-.05-.048-.098-.147-.088-.294a6.1 6.1 0 0 0 0-.772c-.01-.147.039-.246.088-.294l.814-.806c.475-.469.679-1.216.364-1.891a7.992 7.992 0 0 0-.704-1.218c-.428-.609-1.176-.806-1.82-.63l-1.103.303c-.066.019-.176.011-.299-.071a5.991 5.991 0 0 0-.668-.386c-.133-.066-.194-.158-.212-.224L10.16 1.29C9.99.645 9.444.095 8.701.031A8.094 8.094 0 0 0 8 0zm1.5 8a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0zM11 8a3 3 0 1 1-6 0 3 3 0 0 1 6 0z"></path></svg></span>
			<strong>Modular & Extensible</strong>
		</p>
		<hr class="pillarseparator" />
        <p>
			Minimal core. Does nothing unnecessary.<br/>
			All game modifications performed via mods.	
		</p>
  	</div>
</div>

<!-- Rust/C# & Perf -->
<div class="pillarwrapper">
    <div class="pillarcard">
		<p class="pillartitle">
			<span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="m11.5 15.97.41 2.44c-.26.14-.68.27-1.24.39-.57.13-1.24.2-2.01.2-2.21-.04-3.87-.7-4.98-1.96C2.56 15.77 2 14.16 2 12.21c.05-2.31.72-4.08 2-5.32C5.32 5.64 6.96 5 8.94 5c.75 0 1.4.07 1.94.19s.94.25 1.2.4l-.58 2.49-1.06-.34c-.4-.1-.86-.15-1.39-.15-1.16-.01-2.12.36-2.87 1.1-.76.73-1.15 1.85-1.18 3.34 0 1.36.37 2.42 1.08 3.2.71.77 1.71 1.17 2.99 1.18l1.33-.12c.43-.08.79-.19 1.1-.32M13.89 19l.61-4H13l.34-2h1.5l.32-2h-1.5L14 9h1.5l.61-4h2l-.61 4h1l.61-4h2l-.61 4H22l-.34 2h-1.5l-.32 2h1.5L21 15h-1.5l-.61 4h-2l.61-4h-1l-.61 4h-2m2.95-6h1l.32-2h-1l-.32 2z"></path></svg></span>
			<strong>Write Memory Safe Mods</strong>
		</p>
		<hr class="pillarseparator" />
        <p>
			Fast development time with easy to learn C#.<br/>
            Or Rust for wider platform support.
		</p>
    </div>

    <div class="pillarcard">
		<p class="pillartitle">
			<span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 16a3 3 0 0 1-3-3c0-1.12.61-2.1 1.5-2.61l9.71-5.62-5.53 9.58c-.5.98-1.51 1.65-2.68 1.65m0-13c1.81 0 3.5.5 4.97 1.32l-2.1 1.21C14 5.19 13 5 12 5a8 8 0 0 0-8 8c0 2.21.89 4.21 2.34 5.65h.01c.39.39.39 1.02 0 1.41-.39.39-1.03.39-1.42.01A9.969 9.969 0 0 1 2 13 10 10 0 0 1 12 3m10 10c0 2.76-1.12 5.26-2.93 7.07-.39.38-1.02.38-1.41-.01a.996.996 0 0 1 0-1.41A7.95 7.95 0 0 0 20 13c0-1-.19-2-.54-2.9L20.67 8C21.5 9.5 22 11.18 22 13z"></path></svg></span>
			<strong>High Performance</strong>
		</p>
		<hr class="pillarseparator" />
        <p>
			Modern runtimes, high perf libraries, fast startup times.<br/>
			Built for performance.
		</p>
    </div>
</div>

<!-- Logging & Dependencies -->
<div class="pillarwrapper">
    <div class="pillarcard">
		<p class="pillartitle">
			<span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="m19 23.3-.6-.5c-2-1.9-3.4-3.1-3.4-4.6 0-1.2 1-2.2 2.2-2.2.7 0 1.4.3 1.8.8.4-.5 1.1-.8 1.8-.8 1.2 0 2.2.9 2.2 2.2 0 1.5-1.4 2.7-3.4 4.6l-.6.5M18 2c1.1 0 2 .9 2 2v9.08L19 13l-1 .08V4h-5v8l-2.5-2.25L8 12V4H6v16h7.08c.12.72.37 1.39.72 2H6c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h12Z"/></svg></span>
			<strong>Integrated Logging</strong>
		</p>
		<hr class="pillarseparator" />
        <p>
			Logs to console and file in real time.<br/>
			And perhaps with a universal mod, to the screen too!	
		</p>
  	</div>

	<div class="pillarcard">
		<p class="pillartitle">
			<span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M6.122.392a1.75 1.75 0 0 1 1.756 0l5.25 3.045c.54.313.872.89.872 1.514V7.25a.75.75 0 0 1-1.5 0V5.677L7.75 8.432v6.384a1 1 0 0 1-1.502.865L.872 12.563A1.75 1.75 0 0 1 0 11.049V4.951c0-.624.332-1.2.872-1.514L6.122.392zM7.125 1.69l4.63 2.685L7 7.133 2.245 4.375l4.63-2.685a.25.25 0 0 1 .25 0zM1.5 11.049V5.677l4.75 2.755v5.516l-4.625-2.683a.25.25 0 0 1-.125-.216zm11.672-.282a.75.75 0 1 0-1.087-1.034l-2.378 2.5a.75.75 0 0 0 0 1.034l2.378 2.5a.75.75 0 1 0 1.087-1.034L11.999 13.5h3.251a.75.75 0 0 0 0-1.5h-3.251l1.173-1.233z"></path></svg></span>
			<strong>Dependency System</strong>
		</p>
		<hr class="pillarseparator" />
        <p>
			Mods can set requirements on other mods.<br/>
			The loader will ensure they're loaded before your mod.	
		</p>
  	</div>
</div>

<!-- Early Hook & Hot Reload -->
<div class="pillarwrapper">
    <div class="pillarcard">
		<p class="pillartitle">
			<span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M16.5 5.5a2 2 0 0 0 2-2 2 2 0 0 0-2-2 2 2 0 0 0-2 2 2 2 0 0 0 2 2m-3.6 13.9 1-4.4 2.1 2v6h2v-7.5l-2.1-2 .6-3A7.298 7.298 0 0 0 22 13v-2c-1.76.03-3.4-.89-4.3-2.4l-1-1.6c-.36-.6-1-1-1.7-1-.3 0-.5.1-.8.1L9 8.3V13h2V9.6l1.8-.7-1.6 8.1-4.9-1-.4 2 7 1.4M4 9a1 1 0 0 1-1-1 1 1 0 0 1 1-1h3v2H4m1-4a1 1 0 0 1-1-1 1 1 0 0 1 1-1h5v2H5m-2 8a1 1 0 0 1-1-1 1 1 0 0 1 1-1h4v2H3z"></path></svg></span>
			<strong>Early Hook</strong>
		</p>
		<hr class="pillarseparator" />
        <p>
			Your code executes before the game<br/> 
			runs a single line of code.
		</p>
    </div>

	<div class="pillarcard">
		<p class="pillartitle">
			<span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M17.66 11.2c-.23-.3-.51-.56-.77-.82-.67-.6-1.43-1.03-2.07-1.66C13.33 7.26 13 4.85 13.95 3c-.95.23-1.78.75-2.49 1.32-2.59 2.08-3.61 5.75-2.39 8.9.04.1.08.2.08.33 0 .22-.15.42-.35.5-.23.1-.47.04-.66-.12a.58.58 0 0 1-.14-.17c-1.13-1.43-1.31-3.48-.55-5.12C5.78 10 4.87 12.3 5 14.47c.06.5.12 1 .29 1.5.14.6.41 1.2.71 1.73 1.08 1.73 2.95 2.97 4.96 3.22 2.14.27 4.43-.12 6.07-1.6 1.83-1.66 2.47-4.32 1.53-6.6l-.13-.26c-.21-.46-.77-1.26-.77-1.26m-3.16 6.3c-.28.24-.74.5-1.1.6-1.12.4-2.24-.16-2.9-.82 1.19-.28 1.9-1.16 2.11-2.05.17-.8-.15-1.46-.28-2.23-.12-.74-.1-1.37.17-2.06.19.38.39.76.63 1.06.77 1 1.98 1.44 2.24 2.8.04.14.06.28.06.43.03.82-.33 1.72-.93 2.27z"></path></svg></span>
			<strong>Hot Reload</strong>
		</p>
		<hr class="pillarseparator" />
        <p>
			Load & Unload supported mods at runtime.<br/>
			Or even remotely, APIs available!
		</p>
  	</div>
</div>

<!-- Debugging & Code Safety -->
<div class="pillarwrapper">
    <div class="pillarcard">
		<p class="pillartitle">
			<span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 14a2 2 0 0 1 2 2 2 2 0 0 1-2 2 2 2 0 0 1-2-2 2 2 0 0 1 2-2m11.46-5.14-1.59 6.89L15 14.16l3.8-2.38A7.972 7.972 0 0 0 12 8c-3.95 0-7.23 2.86-7.88 6.63l-1.97-.35C2.96 9.58 7.06 6 12 6c3.58 0 6.73 1.89 8.5 4.72l2.96-1.86z"></path></svg></span>
			<strong>Debugging Support</strong>
		</p>
		<hr class="pillarseparator" />
        <p>
			Debug &amp; Profile your code in Major IDEs<br/> 
			Including Edit &amp; Continue Support<sup id="fnref:1"><a class="footnote-ref" href="#fn:1">1</a></sup>.
		</p>
    </div>

	<div class="pillarcard">
		<p class="pillartitle">
			<span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 12h7c-.53 4.11-3.28 7.78-7 8.92V12H5V6.3l7-3.11M12 1 3 5v6c0 5.55 3.84 10.73 9 12 5.16-1.27 9-6.45 9-12V5l-9-4z"></path></svg></span>
			<strong>Library Conflict Safety</strong>
		</p>
		<hr class="pillarseparator" />
        <p>
			Mods are stored and executed in isolation.<br/>
			Use dynamically linked 3rd party libraries without worrying.
		</p>
  	</div>
</div>

<!-- Any Language, Any Game -->
<div class="pillarwrapper">
    <div class="pillarcard">
		<p class="pillartitle">
			<span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="m14.6 16.6 4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4m-5.2 0L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4Z"></path></svg></span>
			<strong>Use Any Language</strong>
		</p>
		<hr class="pillarseparator" />
        <p>
			Can your language interop with C?<br/>
			Congrats, you're 100% supported.
		</p>
    </div>

    <div class="pillarcard">
		<p class="pillartitle">
			<span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M6 9h2v2h2v2H8v2H6v-2H4v-2h2V9m12.5 0a1.5 1.5 0 0 1 1.5 1.5 1.5 1.5 0 0 1-1.5 1.5 1.5 1.5 0 0 1-1.5-1.5A1.5 1.5 0 0 1 18.5 9m-3 3a1.5 1.5 0 0 1 1.5 1.5 1.5 1.5 0 0 1-1.5 1.5 1.5 1.5 0 0 1-1.5-1.5 1.5 1.5 0 0 1 1.5-1.5M17 5a7 7 0 0 1 7 7 7 7 0 0 1-7 7c-1.96 0-3.73-.8-5-2.1A6.96 6.96 0 0 1 7 19a7 7 0 0 1-7-7 7 7 0 0 1 7-7h10M7 7a5 5 0 0 0-5 5 5 5 0 0 0 5 5c1.64 0 3.09-.79 4-2h2c.91 1.21 2.36 2 4 2a5 5 0 0 0 5-5 5 5 0 0 0-5-5H7Z"></path></svg></span>
			<strong>Add Mod Support Fast</strong>
		</p>
		<hr class="pillarseparator" />
        <p>
			New game? Don't make a loader from scratch.<br/>
			Your game engine might already have modules ready to go.
		</p>
    </div>
</div>

<!-- Any Language, Any Game -->
<div class="pillarwrapper">
    <div class="pillarcard">
		<p class="pillartitle">
			<span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M13 12h7v1.5h-7m0-4h7V11h-7m0 3.5h7V16h-7m8-12H3a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2h18a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2m0 15h-9V6h9"></path></svg></span>
			<strong>Rich Documentation</strong>
		</p>
		<hr class="pillarseparator" />
        <p>
			Writing mods should be easy!<br/> 
			Think <a href="https://reloaded-project.github.io/Reloaded-II/DevelopmentEnvironmentSetup/">Reloaded II Docs</a> but for all languages.
		</p>
    </div>
</div>

The goal is to create a world where modders can focus on actually *modding* the games.  

## Mod Management & Packaging

!!! info

    Mod Managers implementing the R3 standard guarantee the following.

<!-- Clean Install & 1-Click -->
<div class="pillarwrapper">
    <div class="pillarcard">
		<p class="pillartitle">
			<span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><!--! Font Awesome Free 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free (Icons: CC BY 4.0, Fonts: SIL OFL 1.1, Code: MIT License) Copyright 2022 Fonticons, Inc.--><path d="M224 256c-35.2 0-64 28.8-64 64s28.8 64 64 64 64-28.8 64-64-28.8-64-64-64zm209.1-126.9-83.9-83.9c-8.1-8.14-20.4-13.2-33.1-13.2H64C28.65 32 0 60.65 0 96v320c0 35.35 28.65 64 64 64h320c35.35 0 64-28.65 64-64V163.9c0-12.7-5.1-25-14.9-34.8zM128 80h144v80H128V80zm272 336c0 8.836-7.164 16-16 16H64c-8.836 0-16-7.164-16-16V96c0-8.838 7.164-16 16-16h16v104c0 13.25 10.75 24 24 24h192c13.3 0 24-10.7 24-24V83.88l78.25 78.25c1.15 1.07 1.75 2.67 1.75 4.17V416z"/></svg></span>
			<strong>Clean Installation</strong>
		</p>
		<hr class="pillarseparator" />
        <p>
			Doesn't modify game's existing files.<br/> 
			Self contained. Remove R3 folder and it's gone.
		</p>
    </div>

	<div class="pillarcard">
		<p class="pillartitle">
			<span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M11.25 9.331V.75a.75.75 0 0 1 1.5 0v8.58l1.949-2.11A.75.75 0 1 1 15.8 8.237l-3.25 3.52a.75.75 0 0 1-1.102 0l-3.25-3.52A.75.75 0 1 1 9.3 7.22l1.949 2.111z"></path><path fill-rule="evenodd" d="M2.5 3.75a.25.25 0 0 1 .25-.25h5.5a.75.75 0 1 0 0-1.5h-5.5A1.75 1.75 0 0 0 1 3.75v11.5c0 .966.784 1.75 1.75 1.75h6.204c-.171 1.375-.805 2.652-1.77 3.757A.75.75 0 0 0 7.75 22h8.5a.75.75 0 0 0 .565-1.243c-.964-1.105-1.598-2.382-1.769-3.757h6.204A1.75 1.75 0 0 0 23 15.25V3.75A1.75 1.75 0 0 0 21.25 2h-5.5a.75.75 0 0 0 0 1.5h5.5a.25.25 0 0 1 .25.25v11.5a.25.25 0 0 1-.25.25H2.75a.25.25 0 0 1-.25-.25V3.75zM10.463 17c-.126 1.266-.564 2.445-1.223 3.5h5.52c-.66-1.055-1.098-2.234-1.223-3.5h-3.074z"></path></svg></span>
			<strong>1-Click Downloads</strong>
		</p>
		<hr class="pillarseparator" />
        <p>
            Supports 1-click downloads on supported websites.<br/>
            With backwards compatibility for games' legacy protocols.
		</p>
  	</div>
</div>

<!-- Dependency Resolution & Configuration -->
<div class="pillarwrapper">
    <div class="pillarcard">
		<p class="pillartitle">
			<span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M6.122.392a1.75 1.75 0 0 1 1.756 0l5.25 3.045c.54.313.872.89.872 1.514V7.25a.75.75 0 0 1-1.5 0V5.677L7.75 8.432v6.384a1 1 0 0 1-1.502.865L.872 12.563A1.75 1.75 0 0 1 0 11.049V4.951c0-.624.332-1.2.872-1.514L6.122.392zM7.125 1.69l4.63 2.685L7 7.133 2.245 4.375l4.63-2.685a.25.25 0 0 1 .25 0zM1.5 11.049V5.677l4.75 2.755v5.516l-4.625-2.683a.25.25 0 0 1-.125-.216zm11.672-.282a.75.75 0 1 0-1.087-1.034l-2.378 2.5a.75.75 0 0 0 0 1.034l2.378 2.5a.75.75 0 1 0 1.087-1.034L11.999 13.5h3.251a.75.75 0 0 0 0-1.5h-3.251l1.173-1.233z"></path></svg></span>
			<strong>Dependency Resolution</strong>
		</p>
		<hr class="pillarseparator" />
        <p>
			If a mod requires another mod to function,<br/> 
			it will be automatically downloaded.
		</p>
    </div>

	<div class="pillarcard">
		<p class="pillartitle">
			<span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M21 10.12h-6.78l2.74-2.82c-2.73-2.7-7.15-2.8-9.88-.1a6.887 6.887 0 0 0 0 9.8c2.73 2.7 7.15 2.7 9.88 0 1.36-1.35 2.04-2.92 2.04-4.9h2c0 1.98-.88 4.55-2.64 6.29-3.51 3.48-9.21 3.48-12.72 0-3.5-3.47-3.53-9.11-.02-12.58a8.987 8.987 0 0 1 12.65 0L21 3v7.12M12.5 8v4.25l3.5 2.08-.72 1.21L11 13V8h1.5z"></path></svg></span>
			<strong>Automatic Updates</strong>
		</p>
		<hr class="pillarseparator" />
        <p>
			For everything: Launcher, Loader &amp; Mods.<br/>
			Includes super cool <a href="https://reloaded-project.github.io/Reloaded-II/CreatingRelease/#add-delta-update">Delta Update</a> technology.
		</p>
  	</div>
</div>

<!-- Multi-Game Launcher -->
<div class="pillarwrapper">
    <div class="pillarcard">
		<p class="pillartitle">
			<span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M7.429 1.525a6.593 6.593 0 0 1 1.142 0c.036.003.108.036.137.146l.289 1.105c.147.56.55.967.997 1.189.174.086.341.183.501.29.417.278.97.423 1.53.27l1.102-.303c.11-.03.175.016.195.046.219.31.41.641.573.989.014.031.022.11-.059.19l-.815.806c-.411.406-.562.957-.53 1.456a4.588 4.588 0 0 1 0 .582c-.032.499.119 1.05.53 1.456l.815.806c.08.08.073.159.059.19a6.494 6.494 0 0 1-.573.99c-.02.029-.086.074-.195.045l-1.103-.303c-.559-.153-1.112-.008-1.529.27-.16.107-.327.204-.5.29-.449.222-.851.628-.998 1.189l-.289 1.105c-.029.11-.101.143-.137.146a6.613 6.613 0 0 1-1.142 0c-.036-.003-.108-.037-.137-.146l-.289-1.105c-.147-.56-.55-.967-.997-1.189a4.502 4.502 0 0 1-.501-.29c-.417-.278-.97-.423-1.53-.27l-1.102.303c-.11.03-.175-.016-.195-.046a6.492 6.492 0 0 1-.573-.989c-.014-.031-.022-.11.059-.19l.815-.806c.411-.406.562-.957.53-1.456a4.587 4.587 0 0 1 0-.582c.032-.499-.119-1.05-.53-1.456l-.815-.806c-.08-.08-.073-.159-.059-.19a6.44 6.44 0 0 1 .573-.99c.02-.029.086-.075.195-.045l1.103.303c.559.153 1.112.008 1.529-.27.16-.107.327-.204.5-.29.449-.222.851-.628.998-1.189l.289-1.105c.029-.11.101-.143.137-.146zM8 0c-.236 0-.47.01-.701.03-.743.065-1.29.615-1.458 1.261l-.29 1.106c-.017.066-.078.158-.211.224a5.994 5.994 0 0 0-.668.386c-.123.082-.233.09-.3.071L3.27 2.776c-.644-.177-1.392.02-1.82.63a7.977 7.977 0 0 0-.704 1.217c-.315.675-.111 1.422.363 1.891l.815.806c.05.048.098.147.088.294a6.084 6.084 0 0 0 0 .772c.01.147-.038.246-.088.294l-.815.806c-.474.469-.678 1.216-.363 1.891.2.428.436.835.704 1.218.428.609 1.176.806 1.82.63l1.103-.303c.066-.019.176-.011.299.071.213.143.436.272.668.386.133.066.194.158.212.224l.289 1.106c.169.646.715 1.196 1.458 1.26a8.094 8.094 0 0 0 1.402 0c.743-.064 1.29-.614 1.458-1.26l.29-1.106c.017-.066.078-.158.211-.224a5.98 5.98 0 0 0 .668-.386c.123-.082.233-.09.3-.071l1.102.302c.644.177 1.392-.02 1.82-.63.268-.382.505-.789.704-1.217.315-.675.111-1.422-.364-1.891l-.814-.806c-.05-.048-.098-.147-.088-.294a6.1 6.1 0 0 0 0-.772c-.01-.147.039-.246.088-.294l.814-.806c.475-.469.679-1.216.364-1.891a7.992 7.992 0 0 0-.704-1.218c-.428-.609-1.176-.806-1.82-.63l-1.103.303c-.066.019-.176.011-.299-.071a5.991 5.991 0 0 0-.668-.386c-.133-.066-.194-.158-.212-.224L10.16 1.29C9.99.645 9.444.095 8.701.031A8.094 8.094 0 0 0 8 0zm1.5 8a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0zM11 8a3 3 0 1 1-6 0 3 3 0 0 1 6 0z"></path></svg></span>
			<strong>Built-in Mod Configuration</strong>
		</p>
		<hr class="pillarseparator" />
        <p>
            Unified schema for configuring mods.<br/> 
            Works with any language; changes apply in real time!
		</p>
    </div>

    <div class="pillarcard">
		<p class="pillartitle">
			<span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M7.5 9H2v6h5.5l3-3-3-3M6 13H4v-2h2v2m9-5.5V2H9v5.5l3 3 3-3M11 4h2v2h-2V4M9 16.5V22h6v-5.5l-3-3-3 3m4 3.5h-2v-2h2v2m3.5-11-3 3 3 3H22V9h-5.5m3.5 4h-2v-2h2v2Z"/></svg></span>
			<strong>Multi-Game Manager</strong>
		</p>
		<hr class="pillarseparator" />
        <p>
			Supports multiple games at once.<br/> 
			Only one copy of Mod Manager needed.
		</p>
    </div>
</div>

<!-- Installer -->
<div class="pillarwrapper">
    <div class="pillarcard">
		<p class="pillartitle">
			<span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M13 5v6h1.17L12 13.17 9.83 11H11V5h2m2-2H9v6H5l7 7 7-7h-4V3m4 15H5v2h14v-2z"></path></svg></span>
			<strong>Download From Anywhere</strong>
		</p>
		<hr class="pillarseparator" />
        <p>
			Full support for various download sources, download and update!<br/>
            GameBanana, Nexus, GitHub, NuGet and More!
		</p>
    </div>
</div>

## So What's the Idea?

!!! info

    This page looks [awfully familiar to Reloaded-II](https://reloaded-project.github.io/Reloaded-II/), what's up with that?  

`Reloaded-III` is a specification for an enhanced version of `Reloaded-II`; with a newer config schema, 
design that supports multiple platforms (not just Windows) and the ability to allow anyone write mods in an arbitrary programming
language of their choice. 

It expands the tried and tested Reloaded-II paradigm of having individual mods communicate with each other.  

For example, support for specific games is implemented by talking to existing *other mods* which implement middleware/engine specific features for 
archive formats, utility functions etc.

!!! tip

    Did you know the first mod for [Persona 3 on GameBanana](https://gamebanana.com/games/16613) appeared 
    ***40 minutes*** after the game released on PC?  
    No changes were needed to Reloaded-II Launcher or Loader.  

    This was possible because the game used `.cpk`, an archive format from 
    [CRI Middleware](https://en.wikipedia.org/wiki/CRI_Middleware); for which Reloaded had a [universal mod](https://github.com/Sewer56/CriFs.V2.Hook.ReloadedII) to handle 
    these archives without repacking.  

    All the mod author had to do was set a `dependency` the mod and... that was all, it magically works!

## Feasible?

!!! question

    Whoa, whoa, whoa; isn't that a lot of stuff?  
    Yeppers, the good news is; most of this stuff already exists in Reloaded-II 😉.

## Contributions

Contributions to this specification are **highly encouraged**; feel free to make corrections of any sort, and discuss issues as needed.

[^1]: For .NET you might need to set `COMPLUS_FORCEENC = 1` environment variable.
