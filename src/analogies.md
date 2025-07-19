---
title: Analogies
---

# Analogies made by submitters of briefs for Google v. Oracle

```js
const sql = DuckDBClient.sql({
  extracted_analogies: FileAttachment('./data/extracted_analogies_2025-07-19.csv').csv(),
  latent_scope_input: FileAttachment('./data/latent-scope/omitted_nones/scopes-001-input.parquet').parquet(),
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
WHERE analogy != 'None'
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

```sql id=latent_scope_data_to_plot
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
scope
```

```js 
const latent_scope_data_copy = [...latent_scope_data_to_plot]
```

```js
latent_scope_data_copy
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
clusterCentroids
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
clusterHulls
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