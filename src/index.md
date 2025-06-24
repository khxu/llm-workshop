---
title: "Welcome"
---

# Welcome to the LLM workshop

Please copy/paste your OpenAI API key below. Note: don't make a habit of copy/pasting your API keys into mysterious websites outside of this workshop.

## Step 1: Set your OpenAI API key

```js 
const apiKeyInput = view(Inputs.password({
  label: "OpenAI API Key", 
  placeholder: "Copy/paste your API key",
}));
```

```js
const apiKey = Mutable(localStorage.getItem("apiKey") || "");
const setApiKey = () => {
  apiKey.value = apiKeyInput;
  localStorage.setItem("apiKey", apiKeyInput);
  document.querySelector(".hidden-without-api-key").classList.remove("hide");
}
const clearApiKey = () => {
  apiKey.value = "";
  localStorage.removeItem("apiKey");
}
```

```js
view(Inputs.button([["Save API key", setApiKey], ["Clear API key", clearApiKey]]));
```

API key: ${apiKey.length ? "********" + apiKey.slice(apiKey.length - 4): "Not set"}

<section class="hide hidden-without-api-key">

## Step 2: Try some prompts

```js
if (apiKey.length) {
  document.querySelector(".hidden-without-api-key").classList.remove("hide");
}
```

```js
const promptInput = view(Inputs.textarea({
  label: "Prompt",
  placeholder: "Type your prompt here",
  value: "What is the capital of Italy?",
}));
```

```js
const conversations = Mutable([{
  prompt: "What is the meaning of life?",
  response: "42. Or perhaps, the meaning of life is subjective and varies from person to person.",
}]);
const appendConversation = (conversation) => {
  conversations.value = [...conversations.value, conversation];
};
```

```js
view(Inputs.button([["Send", async () => {
  const openai = new OpenAI({ apiKey, dangerouslyAllowBrowser: true });
  try {
    const response = await openai.chat.completions.create({
      model: "gpt-4o-mini",
      messages: [{ role: "user", content: promptInput }],
    });
    console.log(response.choices[0].message.content);
    appendConversation({
      prompt: promptInput,
      response: response.choices[0].message.content,
    });
  } catch (error) {
    console.error("Error:", error);
  }
}]]));
```

```js
display(html`<table>
  <thead>
    <tr>
      <th>Prompt</th>
      <th>Response</th>
    </tr>
  </thead>
  <tbody>
    ${conversations.map(conversation => html`<tr><td>${conversation.prompt}</td><td>${conversation.response}</td></tr>`)}
  </tbody>
</table>`)
```

```js
view(
  Inputs.button('Export data', {
    reduce: () => {
      // Step 1: Create an anchor element
      const a = document.createElement('a');

      // Step 2: Create a URL for the blob
      const url = URL.createObjectURL(new Blob([d3.csvFormat(conversations)], {
        type: 'text/csv',
      }));

      // Step 3: Set the href attribute of the anchor to the blob's URL
      a.href = url;

      // Step 4: Set the download attribute to the desired file name
      a.download = 'conversations.csv';

      // Step 5: Append the anchor to the document
      document.body.appendChild(a);

      // Step 6: Trigger a click on the anchor
      a.click();

      // Step 7: Remove the anchor from the document
      document.body.removeChild(a);

      // Clean up the URL object
      URL.revokeObjectURL(url);
    },
  })
);
```

</section>

```js
import OpenAI from "npm:openai";
```

<style>
  .hide {
    display: none;
  }
</style>
