// These styles are used in the content of the articles. When you update them, all articles will be updated.
export const styles: {
    [key: string]: string;
} = {
    h2: "text-2xl lg:text-4xl font-bold tracking-tight mt-8 mb-4 text-base-content",
    h3: "text-xl lg:text-2xl font-bold tracking-tight mt-6 mb-3 text-base-content",
    p: "text-base-content/90 leading-relaxed mb-4",
    ul: "list-inside list-disc text-base-content/90 leading-relaxed mb-4",
    li: "list-item",
    // Altnernatively, you can use the library react-syntax-highlighter to display code snippets.
    code: "text-sm font-mono bg-neutral text-neutral-content p-6 rounded-box my-4 overflow-x-scroll select-all",
    codeInline:
        "text-sm font-mono bg-base-300 px-1 py-0.5 rounded-box select-all",
    a: "text-primary hover:text-primary-focus underline transition-colors",
    // CTA button styles
    ctaPrimary: "inline-block px-6 py-3 bg-primary text-primary-content font-semibold rounded-lg hover:bg-primary-focus transition-colors",
    ctaSecondary: "inline-block px-6 py-3 bg-secondary text-secondary-content font-semibold rounded-lg hover:bg-secondary-focus transition-colors",
    ctaTertiary: "inline-block px-6 py-3 bg-base-300 text-base-content font-semibold rounded-lg hover:bg-base-200 transition-colors",
    // Citation styles for numbered references
    citation: "text-xs font-medium text-base-content/70 hover:text-base-content cursor-default",
    referenceSection: "mt-12 pt-8 border-t border-base-300",
    referenceTitle: "text-xl font-bold mb-4 text-base-content",
    referenceList: "space-y-2",
    referenceItem: "text-sm text-base-content/80 leading-relaxed",
    referenceNumber: "font-medium text-base-content/70 mr-2",
    referenceLink: "text-base-content/80 hover:text-primary hover:underline transition-colors",
}; 