# System Player and Remote Commands

## Start with AVKit

`AVPlayerViewController` is the default tvOS playback choice because it
provides the system playback experience and handles most expected remote
controls. Before replacing it, identify the concrete product behavior that its
documented extension points cannot provide. A visual preference alone is not a
sufficient custom-player justification.

AVKit can support metadata, custom information tabs, supporting overlays,
content proposals, navigation markers, and other documented playback features.
Use those extension points before recreating player controls.

## Custom Player Responsibility

When custom playback UI is necessary, one media-control owner must coordinate
the `AVPlayer`, item lifecycle, `MPRemoteCommandCenter` handlers, enabled
commands, `MPNowPlayingInfoCenter` updates, interruption/end-of-item state, and
the destination that regains focus after playback ends. This owner should not
be a view that also owns unrelated browse-screen layout.

The custom path needs explicit handling for applicable play/pause, select,
scrub, skip, previous/next, Menu/Back, controller, and system-media-control
events. Enable only commands that the current item can honor, and remove or
disable handlers as playback ownership changes.

## Feature Gates

HLS, interstitials, Picture in Picture, custom tabs/overlays, content proposals,
and Continuity Camera are feature-specific paths. Record the deployment target,
Apple TV model, stream characteristics, permissions/account state, and whether
physical-device evidence is required before claiming support.
