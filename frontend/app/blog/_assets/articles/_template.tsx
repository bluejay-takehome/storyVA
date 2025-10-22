import { articleType } from "../types";
import { authors, authorSlugs } from "../authors";
import { categories, categorySlugs } from "../categories";
import { styles } from "../styles";
import { Citation, ReferenceList } from "../components/Citation";
// Import your header image here:
// import headerImg from "@/public/blog/your-article-slug/header.png";

/**
 * Template Article
 * 
 * To use this template:
 * 1. Copy this file to a new name: your-article-slug.tsx
 * 2. Update all the placeholder values below
 * 3. Create your references array (see example below)
 * 4. Generate header image: bash -i -c "y-image-gen 'your detailed prompt' /path/to/blog/your-article-slug/header.png"
 * 5. Import the header image (uncomment line above)
 * 6. Add the article to articles/index.ts
 * 7. Run npm run build
 */

// Define your references array for citations
const references = [
  {
    number: 1,
    text: "Example Source - Description of the source",
    url: "https://example.com/source1"
  },
  {
    number: 2,
    text: "Another Source - Another description",
    url: "https://example.com/source2"
  },
  // Add more references as needed
];

const article: articleType = {
  // The unique slug for the URL (no spaces, lowercase, hyphens only)
  slug: "your-article-slug",
  
  // Article title (< 60 characters for optimal SEO)
  title: "Your Amazing Article Title Here",
  
  // Meta description for SEO (< 160 characters, appears in search results)
  description: "A compelling description of your article that explains what readers will learn and why they should read it.",
  
  // Select appropriate categories (you can add multiple)
  categories: [
    categories.find(c => c.slug === categorySlugs.writings)!, // Use for new features
    // categories.find(c => c.slug === categorySlugs.tutorial)!, // Use for tutorials
  ],
  
  // Select the author
  author: authors.find(a => a.slug === authorSlugs.claude)!,
  
  // Publication date (YYYY-MM-DD format)
  publishedAt: "2025-06-30", // Update to your publication date. It is the year 2025.
  
  image: {
    // Uncomment when you add your header image:
    // src: headerImg,
    urlRelative: "/blog/your-article-slug/header.png", // Update with your actual path
    alt: "Descriptive alt text for your header image for accessibility",
  },
  
  // Article content as JSX - use the styles object for consistent formatting
  content: (
    <>
      {/* Introduction section */}
      <section>
        <p className={styles.p}>
          Start with a compelling opening paragraph that hooks the reader and clearly explains what they&apos;ll learn from this article. You can add citations like this<Citation number={1} />.
        </p>
        <p className={styles.p}>
          Add more context or background information here<Citation number={2} />. Keep paragraphs readable and engaging.
        </p>
      </section>

      {/* Main content sections */}
      <section>
        <h2 className={styles.h2}>Your First Main Section</h2>
        <p className={styles.p}>
          Break your content into logical sections with clear headings. Use h2 for main sections.
        </p>
        
        <h3 className={styles.h3}>Subsection If Needed</h3>
        <p className={styles.p}>
          Use h3 for subsections within your main sections.
        </p>
        
        {/* Example of a bulleted list */}
        <ul className={styles.ul}>
          <li className={styles.li}>First important point</li>
          <li className={styles.li}>Second important point</li>
          <li className={styles.li}>Third important point</li>
        </ul>
      </section>

      <section>
        <h2 className={styles.h2}>Another Main Section</h2>
        <p className={styles.p}>
          Continue with more valuable content. You can include <strong>bold text</strong> and <em>italic text</em> for emphasis.
        </p>
        
        {/* Example of code snippet */}
        <div className={styles.code}>
{`// Example code block
const example = {
  property: "value",
  method: () => {
    console.log("This is how you can include code");
  }
};`}
        </div>
        
        <p className={styles.p}>
          You can also include inline code like <code className={styles.codeInline}>npm run build</code> using the codeInline style.
        </p>
      </section>

      <section>
        <h2 className={styles.h2}>Tips and Best Practices</h2>
        <ul className={styles.ul}>
          <li className={styles.li}>Keep paragraphs short and scannable</li>
          <li className={styles.li}>Use headings to break up content</li>
          <li className={styles.li}>Include practical examples when possible</li>
          <li className={styles.li}>End with a clear conclusion or call-to-action</li>
        </ul>
      </section>

      <section>
        <h2 className={styles.h2}>Conclusion</h2>
        <p className={styles.p}>
          Wrap up your article with a strong conclusion that summarizes the key points and gives readers a clear next step or takeaway.
        </p>
        <p className={styles.p}>
          Consider ending with a question, call-to-action, or pointer to related content.
        </p>
      </section>

      {/* References section - automatically styled */}
      <ReferenceList references={references} />
    </>
  ),
};

export default article; 