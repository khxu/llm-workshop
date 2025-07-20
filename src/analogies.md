---
title: Analogies
toc: true
---

# Analogies made by submitters of briefs for Google v. Oracle

```js
const sql = DuckDBClient.sql({
  extracted_analogies: FileAttachment('./data/extracted_analogies_2025-07-19.csv').csv(),
  latent_scope_input: FileAttachment('./data/latent-scope/omitted_nones/scopes-001-input.parquet').parquet(),
  embeddings: FileAttachment('./data/latent-scope/omitted_nones/scopes-001-embeddings.parquet').parquet(),
  user_analogy: [{
    analogy: userAnalogy.analogy,
    embeddings: userAnalogy.embeddings,
  }],
});
```

```sql id=extracted_and_split_analogies display
WITH split_analogies AS (
  SELECT
    split(analogies, '|') AS analogies,
    name,
    in_support_of,
    submitter
  FROM extracted_analogies
),
unnested AS (
  SELECT
    name,
    in_support_of,
    submitter,
    trim(unnest(analogies)) AS analogy
  FROM split_analogies
)

SELECT
  analogy,
  name,
  in_support_of,
  submitter
FROM unnested
WHERE analogy != 'None';
```

```js
view(
  Inputs.button('Export data', {
    reduce: exportDataReducer([...extracted_and_split_analogies], 'extracted_and_split_analogies'),
  })
)
```

## Count of analogies by which party the brief was in support of

```js
Plot.plot({
  marks: [
    Plot.barY([...extracted_and_split_analogies], Plot.groupX({y: "count"}, {x: "in_support_of", fill: "in_support_of"})),
    Plot.ruleY([0], {stroke: "black", strokeWidth: 1}),
  ],
})
```

## Count of analogies by submitter

```js
Plot.plot({
  marginRight: 300,
  y: {
    axis: "right",
  },
  x: {
    axis: "both",
    grid: true,
  },
  marks: [
    Plot.barX([...extracted_and_split_analogies], Plot.groupY({x: "count"}, {y: "submitter", fill: "in_support_of", sort: {y: "-x"}, tip: true,})),
    Plot.ruleY([0], {stroke: "black", strokeWidth: 1}),
  ],
})
```

```sql id=latent_scope_data_to_plot echo display
SELECT *
FROM latent_scope_input
```

```js
function exportDataReducer(data, filename) {
  return () => {
    // Step 1: Create an anchor element
    const a = document.createElement('a');

    // Step 2: Create a URL for the blob
    const url = URL.createObjectURL(new Blob([d3.csvFormat(data)], {
        type: 'text/csv',
    }));

    // Step 3: Set the href attribute of the anchor to the blob's URL
    a.href = url;

    // Step 4: Set the download attribute to the desired file name
    a.download = `${filename}.csv`;

    // Step 5: Append the anchor to the document
    document.body.appendChild(a);

    // Step 6: Trigger a click on the anchor
    a.click();

    // Step 7: Remove the anchor from the document
    document.body.removeChild(a);

    // Clean up the URL object
    URL.revokeObjectURL(url);
  }
}
```

```js
const scope = FileAttachment("data/latent-scope/omitted_nones/scopes-001.json").json()
```

```js 
const latent_scope_data_copy = [...latent_scope_data_to_plot]
```

```js
const clusterCentroids = scope.cluster_labels_lookup.map(cluster => {
    const clusterHullPoints = cluster.hull.map(pointIndex => ({
        x: latent_scope_data_copy[pointIndex].x,
        y: latent_scope_data_copy[pointIndex].y,
    }));
    return {
        label: cluster.label,
        x: d3.mean(clusterHullPoints, d => d.x),
        y: d3.mean(clusterHullPoints, d => d.y),
    }
})
```

```js
const clusterHulls = scope.cluster_labels_lookup.map(cluster => {
    return cluster.hull.map(pointIndex => ({
        x: latent_scope_data_copy[pointIndex].x,
        y: latent_scope_data_copy[pointIndex].y,
    }));
})
```

```js
const hullLinePlots = clusterHulls.map(d => {
    return Plot.line([...d, d[0]], {
        x: "x",
        y: "y",
        opacity: 0.5,
        strokeWidth: 0.5,
    })
});
```

```js 
Plot.plot({
    width: 900,
    height: 900,
    x: {
        axis: null,
    },
    y: {
        axis: null,
    },
    color: {
      legend: true,
    },
    inset: 10,
    marks: [
        Plot.frame(),
        Plot.dot(latent_scope_data_copy, {
            x: "x",
            y: "y",
            fill: "in_support_of",
            r: 2,
            opacity: 0.7,
        }),
        [...hullLinePlots],
        Plot.text(clusterCentroids, {
            x: "x",
            y: "y",
            text: "label",
            fontSize: 10,
            opacity: 0.8,
        }),
        Plot.tip(latent_scope_data_copy, Plot.pointer({
            x: "x",
            y: "y",
            title: d => `Name: ${d.name}\n\nIn Support Of: ${d.in_support_of}\n\nSubmitter: ${d.submitter}\n\nLabel: ${d.label}\n\nAnalogy: ${d.analogy}`,
        })),
    ],
})
```

```js 
Plot.plot({
    width: 900,
    height: 25000,
    marginLeft: 500,
    x: {
        axis: null,
    },
    y: {
        axis: null,
    },
    color: {
      legend: true,
      type: "categorical",
    },
    inset: 10,
    marks: [
        Plot.frame(),
        Plot.dot(latent_scope_data_copy, {
            x: "x",
            y: "y",
            fill: "label",
            r: 5,
            opacity: 0.7,
            fy: "submitter",
        }),
        [...hullLinePlots],
        Plot.text(clusterCentroids, {
            x: "x",
            y: "y",
            text: "label",
            fontSize: 10,
            opacity: 0.8,
        }),
        Plot.tip(latent_scope_data_copy, Plot.pointer({
            x: "x",
            y: "y",
            fy: "submitter",
            title: d => `Name: ${d.name}\n\nIn Support Of: ${d.in_support_of}\n\nSubmitter: ${d.submitter}\n\nLabel: ${d.label}\n\nAnalogy: ${d.analogy}`,
        })),
    ],
})
```

```sql id=embeddings_with_analogies display echo
SELECT name, in_support_of, submitter, analogy, label, embeddings
FROM embeddings
ORDER BY submitter, name;
```

Let's take a look at the first embedding:

```js echo
const first_analogy = [...embeddings_with_analogies][0];
```

```js echo
first_analogy.analogy
```

```js echo
const first_embedding = first_analogy.embeddings;
```

```js echo
first_embedding.data[0].values
```

We can plot those 1,536 numbers that make up the vector in a very dense bar chart to visualize the embedding (h/t [Ian Johnson](https://latent.estate/essays/nav-by-sim)):

<div class="card">

**Analogy:** ${first_analogy.analogy}

<div>${embeddingsPlot(first_embedding)}</div>

</div>

```js
function embeddingsPlot(embeddingToPlot) {
  return Plot.plot({
    height: 200,
    x: {
      axis: null,
    },
    marks: [
      Plot.barY(embeddingToPlot, {
        x: (d, i) => i,
        y: d => d,
        fill: d => d >= 0 ? "steelblue" : "orange",
        tip: true,
      }),
    ]
  });
}
```

We can compare this embedding to others to find semantically similar analogies. A common way to do this is to use [cosine distance](https://en.wikipedia.org/wiki/Cosine_similarity#Cosine_distance) as a similarity measure. I.e., the vectors that are closest to each other in terms of cosine distance should also be the vectors that are closest in meaning. Let's find the 10 most similar analogies to `"We cannot recognize copyright as a game of chess in which the public can be checkmated. Cf. Baker v. Selden [citation omitted]."`:

```js
Plot.plot({
  x: {
    axis: null,
  },
  color: {
    legend: true,
  },
  marginTop: 50,
  marginRight: 100,
  marks: [
    Plot.barY([...top_10_similar_analogies], {
      x: "analogy",
      y: "cosine_distance",
      fill: "in_support_of",
      sort: {x: "y"},
      tip: true,
      title: d => `Analogy: ${d.analogy}\n\nSubmitter: ${d.submitter}\n\nIn Support Of: ${d.in_support_of}\n\nCosine Distance: ${d.cosine_distance.toFixed(4)}`,
    }),
    Plot.ruleY([0], {stroke: "black", strokeWidth: 1}),
  ],
})
```

```sql id=top_10_similar_analogies display echo
WITH embedding_of_interest AS (
  SELECT *
  FROM embeddings
  WHERE analogy = 'We cannot recognize copyright as a game of chess in which the public can be checkmated. Cf. Baker v. Selden [citation omitted].'
),
embeddings_other_than_the_one_of_interest AS (
  SELECT *
  FROM embeddings
  WHERE analogy != 'We cannot recognize copyright as a game of chess in which the public can be checkmated. Cf. Baker v. Selden [citation omitted].'
)

SELECT embeddings_other_than_the_one_of_interest.analogy,
    embeddings_other_than_the_one_of_interest.submitter,
    embeddings_other_than_the_one_of_interest.in_support_of,
    embeddings_other_than_the_one_of_interest.name,
    array_cosine_distance(
      embedding_of_interest.embeddings::FLOAT[1536],
      embeddings_other_than_the_one_of_interest.embeddings::FLOAT[1536]
    ) AS cosine_distance,
  embeddings_other_than_the_one_of_interest.embeddings,
  embedding_of_interest.embeddings AS embedding_of_interest
FROM embeddings_other_than_the_one_of_interest
CROSS JOIN embedding_of_interest
ORDER BY cosine_distance ASC
LIMIT 10;
```

Let's plot the embeddings of these in bar charts as well, but also show the diff between that first embedding and the others:

```js
html`${[...top_10_similar_analogies].map(analogy => html`
  <div class="card">
    <p>
      <strong>Analogy:</strong> ${analogy.analogy}<br>
      <strong>Submitter:</strong> ${analogy.submitter}<br>
      <strong>In Support Of:</strong> ${analogy.in_support_of}<br>
      <strong>Cosine Distance:</strong> ${analogy.cosine_distance.toFixed(4)}<br>
    </p>
    <h2>Embedding for: <code>We cannot recognize copyright as a game of chess in which the public can be checkmated. Cf. Baker v. Selden [citation omitted].</code></h2>
    ${embeddingsPlot(analogy.embeddings)}
    <h2>Embedding for: <code>${analogy.analogy}</code></h2>
    ${embeddingsPlot(first_embedding)}
    <h2>Diff of embeddings</h2>
    ${embeddingsPlot(diffEmbeddings(first_embedding.data[0].values, analogy.embeddings.data[0].values))}
  </div>
`)}`
```

```js
function diffEmbeddings(embedding1, embedding2) {
  return embedding1.map((value, index) => Math.abs(value - embedding2[index]));
}
```

```sql id=top_10_least_similar_analogies display echo
WITH embedding_of_interest AS (
  SELECT *
  FROM embeddings
  WHERE analogy = 'We cannot recognize copyright as a game of chess in which the public can be checkmated. Cf. Baker v. Selden [citation omitted].'
),
embeddings_other_than_the_one_of_interest AS (
  SELECT *
  FROM embeddings
  WHERE analogy != 'We cannot recognize copyright as a game of chess in which the public can be checkmated. Cf. Baker v. Selden [citation omitted].'
)

SELECT embeddings_other_than_the_one_of_interest.analogy,
    embeddings_other_than_the_one_of_interest.submitter,
    embeddings_other_than_the_one_of_interest.in_support_of,
    embeddings_other_than_the_one_of_interest.name,
    array_cosine_distance(
      embedding_of_interest.embeddings::FLOAT[1536],
      embeddings_other_than_the_one_of_interest.embeddings::FLOAT[1536]
    ) AS cosine_distance,
  embeddings_other_than_the_one_of_interest.embeddings,
  embedding_of_interest.embeddings AS embedding_of_interest
FROM embeddings_other_than_the_one_of_interest
CROSS JOIN embedding_of_interest
ORDER BY cosine_distance DESC
LIMIT 10;
```

```js
html`${[...top_10_least_similar_analogies].map(analogy => html`
  <div class="card">
    <p>
      <strong>Analogy:</strong> ${analogy.analogy}<br>
      <strong>Submitter:</strong> ${analogy.submitter}<br>
      <strong>In Support Of:</strong> ${analogy.in_support_of}<br>
      <strong>Cosine Distance:</strong> ${analogy.cosine_distance.toFixed(4)}<br>
    </p>
    <h2>Embedding for: <code>We cannot recognize copyright as a game of chess in which the public can be checkmated. Cf. Baker v. Selden [citation omitted].</code></h2>
    ${embeddingsPlot(analogy.embeddings)}
    <h2>Embedding for: <code>${analogy.analogy}</code></h2>
    ${embeddingsPlot(first_embedding)}
    <h2>Diff of embeddings</h2>
    ${embeddingsPlot(diffEmbeddings(first_embedding.data[0].values, analogy.embeddings.data[0].values))}
  </div>
`)}`
```

```js
html`${d3.groups([...embeddings_with_analogies], d => d.submitter)
  .map(([submitter, analogies]) => html`
    <a href="#${submitter}"><h3 id="${submitter}">${submitter}</h3></a>
    <p>In support of: ${analogies[0].in_support_of}</p>
    ${analogies.map((analogy, i) => html`
      <p><strong>Analogy ${i + 1} - ${analogy.label}:</strong> ${analogy.analogy}</p>
    `)}
    <hr>
  `)}`
```

## Compare your own analogies

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

<section class="hidden-without-api-key">

```js
const promptInput = view(Inputs.textarea({
  label: "Analogy",
  placeholder: "Type your analogy here",
  value: "Like an Ikea manual",
}));
```

```js
if (apiKey.length) {
  document.querySelector(".hidden-without-api-key").classList.remove("hide");
}
```

```js
const like_an_ikea_manual_embedding = FileAttachment("data/output/like_an_ikea_manual_embedding.json").json();
```

```js
const userAnalogy = Mutable({
  analogy: "Like an Ikea manual",
  embeddings: like_an_ikea_manual_embedding,
});
const embedUserAnalogy = (analogy) => {
  userAnalogy.value = analogy;
};
```

```js
view(Inputs.button([["Send", async () => {
  const openai = new OpenAI({ apiKey, dangerouslyAllowBrowser: true });
  try {
    const embedding = await openai.embeddings.create({
      model: "text-embedding-3-small",
      input: promptInput,
      encoding_format: "float",
    });
    console.log("Embedding:", embedding);
    embedUserAnalogy({
      analogy: promptInput,
      embeddings: embedding.data[0].embedding,
    });
  } catch (error) {
    console.error("Error:", error);
  }
}]]));
```

### Your analogy

```sql
SELECT *
FROM user_analogy;
```

### Top 10 similar analogies to your analogy

```js
html`${[...top_10_similar_analogies_to_user_analogy].map(analogy => html`
  <div class="card">
    <p>
      <strong>Analogy:</strong> ${analogy.analogy}<br>
      <strong>Submitter:</strong> ${analogy.submitter}<br>
      <strong>In Support Of:</strong> ${analogy.in_support_of || "Neither"}<br>
      <strong>Cosine Distance:</strong> ${analogy.cosine_distance.toFixed(4)}<br>
    </p>
  </div>
`)}`
```

```sql id=top_10_similar_analogies_to_user_analogy
WITH embedding_of_interest AS (
  SELECT *
  FROM user_analogy
  LIMIT 1
),
embeddings_other_than_the_one_of_interest AS (
  SELECT *
  FROM embeddings
)

SELECT
    embeddings_other_than_the_one_of_interest.submitter,
    embeddings_other_than_the_one_of_interest.in_support_of,
    embeddings_other_than_the_one_of_interest.analogy,
    array_cosine_distance(
      embedding_of_interest.embeddings::FLOAT[1536],
      embeddings_other_than_the_one_of_interest.embeddings::FLOAT[1536]
    ) AS cosine_distance,
FROM embeddings_other_than_the_one_of_interest
CROSS JOIN embedding_of_interest
ORDER BY cosine_distance ASC
LIMIT 10;
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
