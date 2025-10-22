import { authorType } from "./types";
import { socialIcons } from "./social-icons";
import [app name]LogoImg from "@/app/[locale]/blog/_assets/images/authors/[app name]-logo.png";

// These slugs are used to generate pages in the /blog/author/[authorId].js. It's a way to show all articles from an author.
const authorSlugs: {
    [key: string]: string;
} = {
    claude: "claude",
    pranav: "pranav",
};

// All the blog authors data display in the /blog/author/[authorId].js pages.
export const authors: authorType[] = [
    {
        // The slug to use in the URL, from the authorSlugs object above.
        slug: authorSlugs.claude,
        // The name to display in the author's bio. Up to 60 characters.
        name: "Claude",
        // The job to display in the author's bio. Up to 60 characters.
        job: "AI Research Assistant",
        // The description of the author to display in the author's bio. Up to 160 characters.
        description:
            "I am an AI assistant with deep research capabilities developed by Anthropic. I help create insightful content about AI, voice technology, and the future of digital storytelling for the [app name] community.",
        // The avatar of the author to display in the author's bio and avatar badge. It's better to use a local image, but you can also use an external image (https://...)
        avatar: [app name]LogoImg,
        // A list of social links to display in the author's bio.
        socials: [
            {
                name: socialIcons.github.name,
                icon: socialIcons.github.svg,
                url: "https://github.com/anthropics/anthropic-sdk-python",
            },
        ],
    },
    {
        slug: authorSlugs.pranav,
        name: "Pranav",
        job: "Creator of [app name]",
        description:
            "I'm the founder and developer of [app name]. Passionate about AI, voice technology, and making creative tools accessible to everyone. Building the future of storytelling.",
        avatar: [app name]LogoImg,
        socials: [
            {
                name: socialIcons.github.name,
                icon: socialIcons.github.svg,
                url: "https://github.com/pbanuru",
            },
        ],
    },
];

export { authorSlugs }; 