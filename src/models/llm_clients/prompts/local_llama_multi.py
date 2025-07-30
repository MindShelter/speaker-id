local_llama_multi_prompt = """
<|begin_of_text|><|start_header_id|>system<|end_header_id|>
Below is an instruction that describes a task, paired with an input that provides further context.
Write a response that appropriately completes the request.

**Task**: Identify the speaker of the tagged dialogue in the narrative.

**Input**: You are given narrative and dialogue text that includes character names. Dialogue lines that require speaker identification are enclosed within [SPEAKER] tags. Additionally, some dialogue may be enclosed within [SPEAKER_NAME] tags, which explicitly provides the speaker's name for the text enclosed within that tag.

**Guidelines**:
- **Identify the Speaker**: Analyze the surrounding narrative and dialogue to determine who is speaking within the `[SPEAKER]` tags.
- **[SPEAKER_NAME] Tag**: If a [SPEAKER_NAME] tag is present, the text enclosed within that tag is spoken by SPEAKER_NAME.
- **Output Format**: Only output the name of the speaker without any additional text.
- **Consistency**: Ensure that the speaker's name matches exactly how it appears in the narrative (e.g., capitalization).
- **Exclusivity**: Do not infer or introduce characters that are not listed in the provided text.

**Examples**:
---
**Example 1**:
The sun was setting over the horizon, casting a golden glow.
[Alex] "I can't believe it's already evening," [/Alex] Alex remarked.
[SPEAKER] "Time flies when you're having fun." [/SPEAKER]
Taylor smiled.
"Indeed it does."
Output: Taylor
---
**Example 2**:
The team gathered around the conference table, preparing for the meeting.
"Let's review the agenda for today," Sam began.
[SPEAKER] "First, we'll discuss the quarterly results, then move on to project updates." [/SPEAKER]
Jordan nodded.
"Sounds good."
Output: Jordan
---
**Example 3**:
Maria walked into the room, noticing the scattered papers on the desk.
"Have you finished the report?" she asked.
"Almost done, just putting the final touches." John replied.
[SPEAKER] "Great, let me know if you need any help." [/SPEAKER]
Output: Maria
---
<|eot_id|>

<|start_header_id|>user<|end_header_id|>
{}
<|eot_id|>
"""
