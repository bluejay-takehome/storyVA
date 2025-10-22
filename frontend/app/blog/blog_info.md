# [app name] Blog System Documentation

## Overview

The [app name] blog is a **static file-based content management system** built with Next.js 14, offering optimal performance through build-time compilation while maintaining full TypeScript type safety.

**Documentation Structure:**
- **This file (`blog_info.md`)**: High-level architecture, technical overview, and system documentation
- **`HOW_TO_ADD_ARTICLE.md`**: Step-by-step quick reference guide for adding content

## Architecture

### Core Technologies
- **Next.js 14** with App Router and static generation
- **TypeScript** throughout with comprehensive type definitions
- **Static generation** using `generateStaticParams` for all routes
- **Component-based architecture** with reusable UI elements

### Content Storage
- **Modular file structure**: Articles, authors, and categories in separate files
- **Individual article files**: Each article in `/app/blog/_assets/articles/[slug].tsx`
- **Shared definitions**: Types, authors, and categories in dedicated files
- **Barrel aggregation**: All content collected via `/app/blog/_assets/articles/index.ts`
- **No circular dependencies**: Clear dependency hierarchy prevents import cycles
- JSX content embedded directly in article definitions
- No database or external CMS - purely static approach

## Content Management Workflow

For adding new articles, authors, or categories, see the dedicated quick reference guide:
**→ `/app/blog/_assets/articles/HOW_TO_ADD_ARTICLE.md`**

For creating new articles from scratch, use the template:
**→ `/app/blog/_assets/articles/_template.tsx`**

## Header Images & Asset Management

### Image Generation

**Backend Utility for Header Images:**
```bash
# Generate blog header images using the backend image generation utility
bash -i -c "y-image-gen " Highly detailed image generation prompt. Be incredibly detailed in exactly how you want to form this header image. You are an architect, okay? This description can be as long as you want. As detailed as you want. " /path/to/blog/article-slug/header.png"
```

### Image Requirements

- **Format**: PNG recommended for best quality and transparency support
- **Location**: `/public/blog/[article-slug]/header.png`
- **Optimization**: Automatic via Next.js Image component
- **Alt Text**: Required for accessibility compliance
- **Dimensions**: Responsive - optimized for multiple screen sizes

### Image Implementation Pattern

```typescript
// Step 1: Import the image at top of your article file
import articleHeaderImg from "@/public/blog/article-slug/header.png";

// Step 2: Reference in article object
image: {
  src: articleHeaderImg,              // For Next.js Image optimization
  urlRelative: "/blog/article-slug/header.png", // For meta tags and social sharing
  alt: "Descriptive alt text for screen readers"
}
```

## Blog Routes & Navigation

### Available Routes

- **`/blog`** - Blog homepage with article cards and category filtering
- **`/blog/[articleId]`** - Individual article pages with sidebar and related articles
- **`/blog/category/[categoryId]`** - Category-filtered article listings
- **`/blog/author/[authorId]`** - Author profile pages with their published articles

### Navigation Components

- **HeaderBlog**: Responsive blog header with logo, category dropdown, and mobile hamburger menu
- **CardArticle**: Article preview cards with header images, metadata, and descriptions
- **BadgeCategory**: Category tags for filtering and organization
- **Avatar**: Author profile links with images and hover effects

## Current Content Status

### Active Categories (2)
- **"New Features"** (`feature`) - Latest [app name] platform updates and feature announcements
- **"How Tos & Tutorials"** (`tutorial`) - Step-by-step user guides and educational content

### Active Authors (1)
- **"Claude"** - AI Writing Assistant
  - **Role**: Primary content creator
  - **Avatar**: [app name] logo
  - **Social**: GitHub link to Anthropic Claude

### Published Articles (1)
- **"The AI Revolution in Storytelling"** - Comprehensive article covering:
  - AI voice cloning technology in fanfiction
  - Market analysis and user benefits
  - Technical implementation overview
  - Future outlook for AI-powered storytelling

## SEO & Performance Features

### Built-in SEO Optimization

- **JSON-LD structured data** for Google rich snippets and enhanced search results
- **Open Graph meta tags** for Facebook, Discord, and other social platform previews
- **Twitter Card meta tags** for optimized Twitter sharing
- **Canonical URLs** for all pages to prevent duplicate content issues
- **Dynamic meta titles and descriptions** based on article/category/author content
- **Sitemap generation** for search engine crawling and indexing

### Performance Optimizations

- **Static generation** - All pages pre-built at compile time for instant loading
- **Image optimization** - Automatic WebP conversion, responsive images, and lazy loading
- **Priority loading** - Above-the-fold images marked for immediate loading
- **Mobile-first responsive design** with optimized layouts across all screen sizes
- **Code splitting** - Automatic JavaScript chunking for faster page loads

## Technical Implementation

### Type System

All TypeScript type definitions are centralized in `/app/blog/_assets/types.ts`, including:
- `articleType` - Complete article structure with metadata and content
- `categoryType` - Category definitions for filtering and organization
- `authorType` - Author profiles with social links and avatars

### File Structure

```
/app/blog/
   page.tsx                              # Blog homepage
   [articleId]/page.tsx                  # Individual article pages
   category/[categoryId]/page.tsx        # Category listing pages
   author/[authorId]/page.tsx            # Author profile pages
   _assets/
      types.ts                           # Shared TypeScript type definitions
      social-icons.tsx                   # Reusable social media icons
      styles.ts                          # Shared CSS styles for articles
      categories.ts                      # All blog category definitions
      authors.ts                         # All blog author definitions
      articles/                          # Individual article files
          index.ts                       # Barrel file that exports all articles
          _template.tsx                  # Template for new articles
          HOW_TO_ADD_ARTICLE.md          # Quick reference guide
          ai-revolution-fanfiction-storytelling.tsx
      components/                        # Blog-specific components
      images/authors/                    # Author avatar images
   blog_info.md                          # This architecture documentation

/public/blog/
   [article-slug]/header.png             # Article header images
```

## System Characteristics

### Technical Strengths

- **Type safety**: Full TypeScript implementation prevents runtime errors and ensures data consistency
- **Performance**: Optimal loading speeds with static generation and CDN caching
- **SEO**: Comprehensive metadata, structured data, and social sharing optimization
- **Maintainability**: Clean separation of content and presentation logic with modular file structure
- **No circular dependencies**: Clear dependency hierarchy prevents import cycles
- **Better git diffs**: Each article change shows as a single file diff
- **Security**: No database or CMS vulnerabilities - content is compiled into static assets

### Current Limitations

- **Developer-only workflow**: Adding content requires code changes, git commits, and deployment
- **No content scheduling**: All articles are published immediately upon build
- **No draft system**: No preview/staging functionality for content review
- **Single build process**: All content regenerated on each deployment
- **No content versioning**: No ability to revert or track content changes beyond git

### Scalability Considerations

- **Build time**: Increases linearly with article count (currently minimal impact)
- **Image management**: Manual optimization and placement required for each article
- **Content workflow**: Not suitable for non-technical authors or content managers
- **Version control**: All content changes must go through git workflow

## Best Practices

### Content Guidelines

- **Article titles**: Keep under 60 characters for optimal SEO
- **Meta descriptions**: Limit to 160 characters for search snippets
- **Image alt text**: Always provide descriptive alt text for accessibility
- **Content structure**: Use proper heading hierarchy (h2, h3, etc.)
- **Internal linking**: Link to related articles and categories when relevant

### Development Workflow

1. **Create branch** for new content
2. **Add article/author/category** following the quick reference guide
3. **Test locally** with `npm run dev`
4. **Build and verify** with `npm run build`
5. **Commit and deploy** through standard git workflow

### Performance Tips

- **Optimize images** before adding to `/public/blog/`
- **Use descriptive file names** for better SEO
- **Keep article content reasonable** - very long articles may impact build time
- **Test on mobile** - ensure responsive design works for all content

---

**Note**: This static blog system is production-ready and optimal for developer-managed content workflows. The current implementation provides excellent performance, SEO, and maintainability for content that doesn't require frequent updates by non-technical users.