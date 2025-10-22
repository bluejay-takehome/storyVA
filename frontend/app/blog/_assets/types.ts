import type { JSX } from "react";
import { StaticImageData } from "next/image";

export type categoryType = {
    slug: string;
    title: string;
    titleShort?: string;
    description: string;
    descriptionShort?: string;
};

export type authorType = {
    slug: string;
    name: string;
    job: string;
    description: string;
    avatar: StaticImageData | string;
    socials?: {
        name: string;
        icon: JSX.Element;
        url: string;
    }[];
};

export type articleType = {
    slug: string;
    title: string;
    description: string;
    categories: categoryType[];
    author: authorType;
    publishedAt: string;
    image: {
        src?: StaticImageData;
        urlRelative: string;
        alt: string;
    };
    content: JSX.Element;
}; 