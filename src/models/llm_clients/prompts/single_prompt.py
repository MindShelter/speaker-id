single_prompt = """
Below is an instruction that describes a task, paired with an input that provides further context.
Write a response that appropriately completes the request.

**Task**: Identify the speaker of the tagged dialogue in the narrative.

**Input**: You are given narrative and dialogue text that includes character names. Dialogue lines that require speaker identification are enclosed within [SPEAKER] tags.

**Guidelines**:
- **Identify the Speaker**: Analyze the surrounding narrative and dialogue to determine who is speaking within the `[SPEAKER]` tags.
- **Output Format**: Only output the name of the speaker without any additional text.
- **Consistency**: Ensure that the speaker's name matches exactly how it appears in the narrative (e.g., capitalization).
- **Exclusivity**: Do not infer or introduce characters that are not listed in the provided text.

**Examples**:
---
**Example 1**:
The sun was setting over the horizon, casting a golden glow.
"I can't believe it's already evening," Alex remarked.
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
"""
