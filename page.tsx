import Image from 'next/image';
export default function Home(){return <section className="home"><h1 className="sr-only">Elsie Ambrose</h1><Image unoptimized className="home-art" src="/artwork/cloudscape.jpeg" alt="Elsie Ambrose’s painting of turbulent clouds and shafts of light" width={2474} height={1536} fetchPriority="high"/></section>}
