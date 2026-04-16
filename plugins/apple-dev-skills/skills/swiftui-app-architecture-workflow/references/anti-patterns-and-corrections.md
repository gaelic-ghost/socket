# Anti-Patterns And Corrections

## Environment Dumping Ground

Bad shape:

- every dependency gets pushed into environment values or environment objects because it is convenient

Correction:

- keep narrow dependencies explicit
- reserve environment for shared contextual scope that honestly belongs to the hierarchy

## Giant Root View

Bad shape:

- one root view owns app lifecycle concerns, scene wiring, command wiring, transient UI state, and leaf rendering details

Correction:

- split by responsibility
- keep app and scene boundaries explicit
- keep leaf rendering concerns local to smaller composable views

## Wrapper-Heavy Architecture

Bad shape:

- extra coordinators, wrappers, and controller layers are added only to look architectural

Correction:

- prefer direct SwiftUI structure until a concrete ownership or lifecycle problem demands a layer
- make every extra type justify a real boundary

## Preference Keys As A State Bus

Bad shape:

- preference keys are used for ordinary state propagation or service access

Correction:

- use them only for upward publication from descendants to ancestors
- otherwise use explicit state flow or another narrower mechanism

## Hidden Control Flow In Modifiers

Bad shape:

- important app or scene behavior is buried in modifier chains so ownership becomes hard to explain

Correction:

- keep ownership and action flow obvious
- extract structure when needed, but do not hide the real owner

## Leaf Views Owning App Commands

Bad shape:

- command policy and app-level actions are effectively owned by one leaf view

Correction:

- let the command surface own commands
- let leaf views publish focused context when commands need it
