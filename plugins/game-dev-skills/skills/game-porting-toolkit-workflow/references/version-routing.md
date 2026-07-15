# GPTK Version Routing

## Source anchors

- [Game Porting Toolkit](https://developer.apple.com/games/game-porting-toolkit/)
- [Speedrun your game port with agentic coding](https://developer.apple.com/videos/play/wwdc2026/357/)
- [Building your macOS game remotely from your PC](https://developer.apple.com/documentation/TechnologyOverviews/building-your-macos-game-remotely-from-your-pc)
- [Apple Game Porting Toolkit repository](https://github.com/apple/game-porting-toolkit)

GPTK 3 supports the evaluation environment for Windows games, Metal Shader Converter, and remote development tooling. Treat it as an evidence and conversion lane.

GPTK 4 adds Apple-maintained agent skills, command-line GPU capture/debugging tools, and Metal 4 evaluation. Its repository states that its newest agent workflow needs macOS 27, Xcode 27, and GPTK 4; these are beta-sensitive requirements until Apple ships them broadly.

For Codex, install GPTK 4 directly from Apple’s marketplace source. Socket’s router intentionally remains a small compatibility and handoff surface.

## Minimum D3D12 Evaluation Record

Record exact game build, GPTK version, macOS/Xcode version, Apple-silicon model, resolution/settings, and launch command. Then record pass/fail plus artifacts for launch and stable gameplay, graphics/UI, keyboard-mouse/controller input, audio, saves, network-dependent behavior, D3D12 features exercised, and DXIL/Metal Shader Converter failures. Capture a repeatable scripted scene or a fixed-duration representative run with frame time, FPS, GPU time, memory, and obvious hitch notes. This establishes a baseline only; it is not release certification.
