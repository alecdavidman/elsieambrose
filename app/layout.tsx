import type { Metadata } from "next";
import type { ReactNode } from "react";
import "./globals.css";

export const metadata: Metadata = {
  title: "Elsie Ambrose — Artist",
  description:
    "Paintings, drawings, and sculptures by Elsie Ambrose, New York.",
};

const basePath = process.env.NEXT_PUBLIC_BASE_PATH ?? "";

const navigation = [
  { label: "Home", href: "/" },
  { label: "Artwork", href: "/artwork/" },
  { label: "Contact", href: "/contact/" },
  { label: "CV", href: "/cv/" },
];

export default function RootLayout({
  children,
}: Readonly<{ children: ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <a className="skip" href="#main">
          Skip to content
        </a>

        <header className="site-header">
          <a
            className="brand"
            href={`${basePath}/`}
            aria-label="Elsie Ambrose home"
          >
            Elsie Ambrose
          </a>

          <nav aria-label="Main navigation">
            {navigation.map(({ label, href }) => (
              <a key={label} href={`${basePath}${href}`}>
                {label}
              </a>
            ))}
          </nav>
        </header>

        <main id="main">{children}</main>

        <footer className="site-footer">
          <a href="mailto:elsieambrose66@gmail.com">
            elsieambrose66@gmail.com
          </a>
          <span>New York, NY</span>
        </footer>
      </body>
    </html>
  );
}
