# Blog Content Structure

This directory contains the modular blog content structure, organized to prevent circular dependencies and improve maintainability.

## File Structure

```
_assets/
├── types.ts              # Shared TypeScript type definitions
├── social-icons.tsx      # Reusable social media icons
├── styles.ts            # Shared CSS class styles for article content
├── categories.ts        # All blog category definitions
├── authors.ts           # All blog author definitions
├── articles/            # Individual article files
│   ├── index.ts         # Barrel file that exports all articles
│   └── ai-revolution-fanfiction-storytelling.tsx
└── components/          # Blog-specific components
```

## How to Add New Content

### Adding a New Article

1. **Create the article file** in `articles/`:
   ```typescript
   // articles/my-new-article.tsx
   import { articleType } from "../types";
   import { authors, authorSlugs } from "../authors";
   import { categories, categorySlugs } from "../categories";
   import { styles } from "../styles";
   import headerImg from "@/public/blog/my-new-article/header.png";

   const article: articleType = {
     slug: "my-new-article",
     title: "My New Article Title",
     description: "Article description for SEO",
     categories: [categories.find(c => c.slug === categorySlugs.tutorial)!],
     author: authors.find(a => a.slug === authorSlugs.claude)!,
     publishedAt: "2024-01-15",
     image: {
       src: headerImg,
       urlRelative: "/blog/my-new-article/header.png",
       alt: "Descriptive alt text"
     },
     content: (
       <>
         <p className={styles.p}>Your content here...</p>
       </>
     ),
   };

   export default article;
   ```

2. **Add header image**: Place in `/public/blog/my-new-article/header.png`

3. **Update the barrel file** (`articles/index.ts`):
   ```typescript
   // Add export
   export { default as myNewArticle } from "./my-new-article";

   // Add import
   import myNewArticle from "./my-new-article";

   // Add to articles array
   export const articles = [
     aiRevolutionFanfictionStorytelling,
     myNewArticle, // <- Add here
   ];
   ```

4. **Build and deploy**: `npm run build`

### Adding a New Author

1. **Update `authors.ts`**:
   ```typescript
   // Add to authorSlugs
   const authorSlugs = {
     claude: "claude",
     newAuthor: "new-author", // <- Add here
   };

   // Add to authors array
   export const authors = [
     // ... existing authors
     {
       slug: authorSlugs.newAuthor,
       name: "Author Name",
       job: "Author Title",
       description: "Author bio",
       avatar: authorAvatarImg,
       socials: [/* social links */],
     },
   ];
   ```

2. **Add avatar image**: Place in `_assets/images/authors/author-name.png`

### Adding a New Category

1. **Update `categories.ts`**:
   ```typescript
   // Add to categorySlugs
   const categorySlugs = {
     feature: "feature",
     tutorial: "tutorial",
     newCategory: "new-category", // <- Add here
   };

   // Add to categories array
   export const categories = [
     // ... existing categories
     {
       slug: categorySlugs.newCategory,
       title: "New Category Title",
       titleShort: "Short",
       description: "Category description",
       descriptionShoft: "Short description",
     },
   ];
   ```

## Dependency Flow

The structure prevents circular dependencies by maintaining a clear dependency hierarchy:

```
Foundation Layer (no dependencies on each other):
├── types.ts
├── social-icons.tsx
└── styles.ts

Data Layer (imports from Foundation):
├── categories.ts  → types.ts
└── authors.ts     → types.ts, social-icons.tsx

Content Layer (imports from Foundation + Data):
└── articles/
    ├── article1.tsx → types.ts, authors.ts, categories.ts, styles.ts
    └── article2.tsx → types.ts, authors.ts, categories.ts, styles.ts

Aggregation Layer (imports from Content):
└── articles/index.ts → all article files

Application Layer (imports from Aggregation):
└── pages/ → articles/index.ts, categories.ts, authors.ts
```

## Benefits

- **No circular dependencies**: Clear dependency flow prevents import cycles
- **Better git diffs**: Each article change shows as a single file diff
- **Type safety**: Full TypeScript support throughout
- **Easy maintenance**: Isolated files are easier to modify
- **Scalable**: Can handle hundreds of articles without performance issues
- **SEO preserved**: All existing SEO features continue to work

## Migration Notes

- Old `content.tsx` has been backed up as `content.tsx.backup`
- All existing pages automatically updated to use new structure
- Build and runtime behavior remains identical
- No changes needed to components or styling 