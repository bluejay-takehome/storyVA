import Link from "next/link";
import Image from "next/image";
import { articleType } from "../types";
import { useTranslations } from "next-intl";

// This is the author avatar that appears in the article page and in <CardArticle /> component
const Avatar = ({ article }: { article: articleType }) => {
  const t = useTranslations("blog");

  return (
    <Link
      href={`/blog/author/${article.author.slug}`}
      title={t("postsBy", { author: article.author.name })}
      className="inline-flex items-center gap-2 group"
      rel="author"
    >
      <span itemProp="author">
        <Image
          src={article.author.avatar}
          // alt={`Avatar of ${article.author.name}`}
          alt=""
          className="w-7 h-7 rounded-full object-cover object-center"
          width={28}
          height={28}
        />
      </span>
      <span className="group-hover:underline">{article.author.name}</span>
    </Link>
  );
};

export default Avatar;
