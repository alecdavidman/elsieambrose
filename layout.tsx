/* oxlint-disable next/no-html-link-for-pages */
// Native navigation avoids the previously verified production client-router failure.
import type { Metadata } from 'next';
import './globals.css';
export const metadata: Metadata = {title:'Elsie Ambrose — Artist',description:'Paintings, drawings, and sculptures by Elsie Ambrose, New York.'};
export default function Layout({children}:{children:React.ReactNode}){return <html lang="en"><body><a className="skip" href="#main">Skip to content</a><header className="site-header"><a className="brand" href="/">Elsie Ambrose</a><nav aria-label="Main navigation"><a href="/">Home</a><a href="/artwork">Artwork</a><a href="/contact">Contact</a><a href="/cv">CV</a></nav></header><main id="main">{children}</main><footer><a href="mailto:elsieambrose66@gmail.com">elsieambrose66@gmail.com</a><span>New York, NY</span></footer></body></html>}
