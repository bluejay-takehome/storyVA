import Link from "next/link";
import { categoryType } from "../types";
import { useTranslations } from "next-intl";

// This is the category badge that appears in the article page and in <CardArticle /> component
const Category = ({
  category,
  extraStyle,
}: {
  category: categoryType;
  extraStyle?: string;
}) => {
  const t = useTranslations("blog");

  return (
    <Link
      href={`/blog/category/${category.slug}`}
      className={`badge badge-sm md:badge-md hover:badge-primary ${
        extraStyle ? extraStyle : ""
      }`}
      title={t("postsIn", { category: category.title })}
      rel="tag"
    >
      {category.titleShort}
    </Link>
  );
};

export default Category;
