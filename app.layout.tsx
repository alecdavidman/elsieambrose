import './globals.css'; // This links your Tailwind styles

export const metadata = {
  title: 'Elsie Ambrose — Portfolio',
  description: 'Complete published source artwork collection',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <main>{children}</main>
      </body>
    </html>
  );
}
