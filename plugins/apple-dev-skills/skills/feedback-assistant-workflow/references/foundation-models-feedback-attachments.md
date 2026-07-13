# Foundation Models Feedback Attachments

`LanguageModelFeedback` describes structured Foundation Models feedback. `LanguageModelSession.logFeedbackAttachment(sentiment:issues:desiredOutput:)` returns JSON `Data` that includes session transcript material, feedback sentiment, identified issues, and optional desired output.

```swift
let attachment = session.logFeedbackAttachment(
    sentiment: .negative,
    issues: [
        .init(category: .incorrect, explanation: "State the observed mismatch.")
    ],
    desiredOutput: expectedResponse
)
try attachment.write(to: feedbackURL)
```

This API creates an attachment only. It does not create or submit a Feedback Assistant report. Review the resulting JSON for prompts, responses, or other private content before saving it or attaching it to Feedback Assistant.

Apple documents that multiple feedback attachments can be combined in one JSON file, but only combine artifacts that belong to the same report and have passed the same privacy review.

## Sources

- Apple Developer, [`LanguageModelFeedback`](https://developer.apple.com/documentation/foundationmodels/languagemodelfeedback)
- Apple Developer, [`logFeedbackAttachment(sentiment:issues:desiredOutput:)`](https://developer.apple.com/documentation/foundationmodels/languagemodelsession/logfeedbackattachment(sentiment:issues:desiredoutput:))
