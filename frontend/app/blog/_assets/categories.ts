import { categoryType } from "./types";

// These slugs are used to generate pages in the /blog/category/[categoryI].js. It's a way to group articles by category.
const categorySlugs: { [key: string]: string } = {
    feature: "feature",
    tutorial: "tutorial",
    writings: "writings",
};

// All the blog categories data display in the /blog/category/[categoryI].js pages.
export const categories: categoryType[] = [
    {
        // The slug to use in the URL, from the categorySlugs object above.
        slug: categorySlugs.feature,
        // The title to display the category title (h1), the category badge, the category filter, and more. Less than 60 characters.
        title: "New Features",
        // A short version of the title above, display in small components like badges. 1 or 2 words
        titleShort: "Features",
        // The description of the category to display in the category page. Up to 160 characters.
        description:
            "Here are the latest features we've added to [app name]. I'm constantly improving our AI voice cloning platform to help you create better audio stories.",
        // A short version of the description above, only displayed in the <Header /> on mobile. Up to 60 characters.
        descriptionShort: "Latest features added to [app name].",
    },
    {
        slug: categorySlugs.tutorial,
        title: "How Tos & Tutorials",
        titleShort: "Tutorials",
        description:
            "Learn how to use [app name] with these step-by-step tutorials. I'll show you how to create amazing AI-generated audiobooks from your stories.",
        descriptionShort:
            "Learn how to use [app name] with these step-by-step tutorials.",
    },
    {
        slug: categorySlugs.writings,
        title: "Fanfiction & Creative Writing",
        titleShort: "Writings",
        description:
            "Explore the world of fanfiction, creative writing, and storytelling. Discover insights about the community, barriers, and how AI is transforming the way we create and consume stories.",
        descriptionShort: "Fanfiction, creative writing, and storytelling insights.",
    },
];

export { categorySlugs }; 