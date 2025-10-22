@_template.tsx  @HOW_TO_ADD_ARTICLE.md 

Can you turn this into an article? And make sure to add any sort of text formatting, any sort of custom inline visuals, anything that will make this easy to understand and process and read, you know. I provided you the markdown, but what we need is TSX. You will need to add formatting, bolding, italicization, etc.


# How to Add a New Blog Article

This guide explains how to add a new article to the [app name] blog using our citation system.

## Step 1: Create Article File

Create a new file in `/articles/` with the naming convention: `your-article-slug.tsx`

## Step 2: Set Up Article Structure

Copy the structure from `_template.tsx` and modify it for your article.

## Step 3: Citation System

We use a numbered citation system similar to academic papers. Here's how it works:

### Adding Citations

1. **Create references array** with all your sources:
```tsx
const references = [
  {
    number: 1,
    text: "Wikipedia - Example Topic",
    url: "https://en.wikipedia.org/wiki/Example"
  },
  {
    number: 2,
    text: "Research Paper Title - Journal Name",
    url: "https://example.com/paper"
  },
];
```

2. **Use Citation components** in your text:
```tsx
<p className={styles.p}>
  This statement needs a citation<Citation number={1} /> and this one too<Citation number={2} />.
</p>
```

3. **Add reference list** at the end:
```tsx
<ReferenceList references={references} />
```

### Interactive Citations

The citation system is fully interactive:
- **Clicking a citation number** (e.g., `[1]`) smoothly scrolls to the corresponding reference
- **References are highlighted** briefly when clicked to
- **Hover tooltip** shows "Go to reference X"
- **External links** in reference list open in new tabs

### Citation Best Practices

- **Number consecutively** starting from 1
- **Reuse numbers** for the same source if cited multiple times
- **Use descriptive text** in references (not just "Link" or "Website")
- **Include publication name** where relevant (e.g., "Wikipedia - Topic" or "Journal Name - Article Title")
- **Keep citations close** to the relevant claim, not at end of paragraph

### Example Citation Usage

```tsx
// Single citation
<p>Edison invented the phonograph in 1877<Citation number={1} />.</p>

// Multiple citations
<p>Several studies confirm this<Citation number={2} /><Citation number={3} /><Citation number={4} />.</p>

// Reusing citations
<p>As mentioned earlier<Citation number={1} />, Edison's invention was revolutionary.</p>
```

## Step 4: Header Image

Create a header image and place it in `/public/blog/your-article-slug/header.png`

For AI-generated images, use detailed prompts covering:
- Main subject and setting
- Art style (photorealistic, illustration, etc.)
- Color scheme and lighting
- Aspect ratio (typically 16:9 landscape)

## Step 5: Content Guidelines

- Use the provided styles (`styles.p`, `styles.h2`, etc.)
- Structure content with clear sections
- Include engaging introduction and conclusion
- Add citations for all factual claims
- Keep paragraphs readable (3-5 sentences max)

## Step 6: Add to Index

Add your article to `/articles/index.ts`:

```tsx
// Export individual articles
export { default as yourArticleSlug } from "./your-article-slug";

// Import all articles
import yourArticleSlug from "./your-article-slug";

// Add to articles array
export const articles: articleType[] = [
    yourArticleSlug,
    // ... other articles
];
```

## Step 7: Test

1. **Build the project**: `npm run build`
2. **Check for errors** in the terminal output
3. **View locally**: `npm run dev` and navigate to `/blog/your-article-slug`

## Common Issues

- **Missing citations**: Build will fail if Citation components reference non-existent numbers
- **Image not found**: Ensure header image path matches exactly
- **TypeScript errors**: Check that all required article properties are included
- **Client component errors**: Citation components require 'use client' directive (already included)

## File Checklist

Before submitting:
- [ ] Article file created in `/articles/`
- [ ] Header image added to `/public/blog/article-slug/`
- [ ] Article exported in `/articles/index.ts`
- [ ] All citations numbered and referenced properly
- [ ] Build completes without errors

## Quick Steps

1. **Copy the template**
   ```bash
   cp _template.tsx your-article-slug.tsx
   ```

2. **Generate header image**
   ```bash
   # Use the y-image-gen alias to create your header image
   bash -i -c "y-image-gen 'Highly detailed image generation prompt. Be incredibly detailed in exactly how you want to form this header image. You are an architect, okay? This description can be as long as you want. As detailed as you want.' /public/blog/your-article-slug/header.png"
   ```

   # if asking ai to generate an image prompt:
   ```bash
   If you could create a highly detailed image prompt for an image that will be the header image for this blog post, what would you write in that prompt? This is a prompt for an AI image generator. And you can be incredibly detailed. This technology has gone a long way, so you can describe every single facet of the image using as many words as you would like to, and being extremely detailed, like a precision architect.
   ```

3. **Edit the article file**
   - View the template file to see the structure and available styles at `[app name]/app/blog/_assets/articles/_template.tsx` and `[app name]/app/blog/_assets/styles.ts`
   - Feel free to add new styles if they would be beneficial for future articles in `styles.ts`
   - Update the slug, title, description
   - Uncomment and fix the header image import
   - Write your content using the provided structure, ensure to escape special characters. 
   - MAKE SURE TO INCLUDE CITATIONS.
   - Choose appropriate categories and author

4. **Add to barrel file** (`index.ts`)
   ```typescript
   // Add export
   export { default as yourArticleSlug } from "./your-article-slug";

   // Add import
   import yourArticleSlug from "./your-article-slug";

   // Add to articles array
   export const articles = [
     aiRevolutionFanfictionStorytelling,
     yourArticleSlug, // <- Add here
   ];
   ```

5. **Build and test**
   ```bash
   npm run build
   npm run dev  # Test locally at http://localhost:3000/blog
   ```

## Content Guidelines

### SEO Best Practices
- **Title**: < 60 characters
- **Description**: < 160 characters
- **Alt text**: Descriptive for all images
- **Headings**: Use proper hierarchy (h2, h3)

### Writing Style
- Start with a compelling hook
- Break content into scannable sections
- Use bullet points for lists
- Include practical examples
- End with clear takeaways

### Available Styles
```typescript
styles.h2          // Main section headings
styles.h3          // Subsection headings  
styles.p           // Paragraphs
styles.ul          // Unordered lists
styles.li          // List items
styles.code        // Code blocks
styles.codeInline  // Inline code
// Citation styles (use Citation component instead)
styles.citation    // Superscript citation numbers
styles.referenceSection // Reference list container
styles.referenceTitle   // "References" heading
styles.referenceList    // Reference list styling
styles.referenceItem    // Individual reference styling
styles.referenceNumber  // Reference number styling
styles.referenceLink    // Reference link styling
```

### Citations and References

Use numbered superscript citations for better readability:

**Import the citation components:**
```typescript
import { Citation, ReferenceList } from "../components/Citation";
```

**In your article content:**
```typescript
<p className={styles.p}>
  This is a fact that needs a citation<Citation number={1} />. 
  Here's another fact<Citation number={2} />.
</p>
```

**Create your references array:**
```typescript
const references = [
  {
    number: 1,
    text: "Wikipedia - Audiobook History",
    url: "https://en.wikipedia.org/wiki/Audiobook"
  },
  {
    number: 2,
    text: "Grand View Research - Audiobook Market Analysis",
    url: "https://www.grandviewresearch.com/industry-analysis/audiobooks-market"
  }
];
```

**Add reference list at the end of content:**
```typescript
content: (
  <>
    {/* Your article content with <Citation number={1} /> etc. */}
    
    <ReferenceList references={references} />
  </>
)
```

**Tips for citations:**
- Number citations sequentially as they appear in the text
- Reuse the same number for repeated sources
- Keep reference text descriptive but concise
- Always include the full URL
- Group all references at the end for easy management

### Categories
- `categorySlugs.feature` - For new features and announcements
- `categorySlugs.tutorial` - For how-to guides and tutorials
- `categorySlugs.writings` - For other writings

### Authors
- `authorSlugs.claude` - AI Writing Assistant

## Header Image Generation

Use the `y-image-gen` alias to create professional header images:

```bash
bash -i -c "y-image-gen 'A detailed prompt describing your header image. Include visual style, composition, colors, elements, mood, and any specific details you want. Be as descriptive as possible for best results.' /public/blog/your-article-slug/header.png"
```

**Tips for good prompts:**
- Be specific about visual style (modern, minimalist, tech-focused, etc.)
- Include composition details (centered text, abstract background, etc.)
- Mention colors and mood
- Describe any specific elements related to your article topic

## File Naming Convention
- Use kebab-case: `my-awesome-article.tsx`
- No spaces, special characters, or uppercase
- Keep URLs readable and SEO-friendly 