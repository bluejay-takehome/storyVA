'use client';

import React from 'react';

interface CitationProps {
  number: number;
  className?: string;
}

/**
 * Citation component for numbered superscript citations
 * Usage: <Citation number={1} />
 */
export const Citation: React.FC<CitationProps> = ({ number, className = "" }) => {
  const handleClick = () => {
    const referenceElement = document.getElementById(`ref-${number}`);
    if (referenceElement) {
      referenceElement.scrollIntoView({ 
        behavior: 'smooth', 
        block: 'center' 
      });
      // Add a subtle highlight effect
      referenceElement.classList.add('bg-yellow-100');
      setTimeout(() => {
        referenceElement.classList.remove('bg-yellow-100');
      }, 2000);
    }
  };

  return (
    <sup 
      className={`text-xs font-medium text-primary hover:text-primary-focus cursor-pointer transition-colors ${className}`}
      onClick={handleClick}
      title={`Go to reference ${number}`}
    >
      [{number}]
    </sup>
  );
};

interface ReferenceListProps {
  references: Array<{
    number: number;
    text: string;
    url: string;
  }>;
  className?: string;
}

/**
 * Reference list component for the bottom of articles
 * Usage: <ReferenceList references={referencesArray} />
 */
export const ReferenceList: React.FC<ReferenceListProps> = ({ references, className = "" }) => {
  return (
    <section className={`mt-12 pt-8 border-t border-base-300 ${className}`}>
      <h2 className="text-xl font-bold mb-4 text-base-content">References</h2>
      <ol className="space-y-2">
        {references.map((ref) => (
          <li 
            key={ref.number} 
            id={`ref-${ref.number}`}
            className="text-sm text-base-content/80 leading-relaxed transition-colors duration-500 rounded p-2"
          >
            <span className="font-medium text-base-content/70 mr-2">[{ref.number}]</span>
            <a 
              href={ref.url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-base-content/80 hover:text-primary hover:underline transition-colors"
            >
              {ref.text}
            </a>
          </li>
        ))}
      </ol>
    </section>
  );
}; 