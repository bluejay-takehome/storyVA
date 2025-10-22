// Export individual articles
// export { default as how[app name]Works } from "./how-x-works";

// Import all articles to create the articles array

// import howXWorks from "./how-x-works";
import { articleType } from "../types";

// Export the articles array for pages that need it
export const articles: articleType[] = [
    // howXWorks,
];

// Note: When adding new articles, follow this pattern:
// 1. Export the default export with a descriptive name
// 2. Import it in the second section
// 3. Add it to the articles array 