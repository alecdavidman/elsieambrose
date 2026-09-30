/* oxlint-disable next/no-html-link-for-pages */
// Native links avoid a verified production failure in the Vinext client router.
'use client';
import Image from 'next/image';

import {useEffect,useRef,useState} from 'react';
import {Carousel,CarouselContent,CarouselItem,type CarouselApi} from '@/components/ui/carousel';
import type {Collection} from './collections';
export default function CollectionViewer({collection}:{collection:Collection}){
 const [api,setApi]=useState<CarouselApi>();
 const [selected,setSelected]=useState(0);
 const thumbs=useRef<(HTMLButtonElement|null)[]>([]);
 const strip=useRef<HTMLFieldSetElement>(null);
 const current=collection.items[selected];
 useEffect(()=>{if(!api)return;const update=()=>setSelected(api.selectedScrollSnap());update();api.on('select',update);api.on('reInit',update);return()=>{api.off('select',update);api.off('reInit',update)}},[api]);
 useEffect(()=>{const button=thumbs.current[selected],row=strip.current;if(button&&row){const left=button.offsetLeft-row.offsetLeft;if(left<row.scrollLeft||left+button.offsetWidth>row.scrollLeft+row.clientWidth)row.scrollTo({left:left-row.clientWidth/2+button.offsetWidth/2,behavior:'instant'});}},[selected]);
 return <section className="collection-page"><div className="collection-heading"><a className="label" href="/artwork">All artwork</a><h1>{collection.title}</h1></div><Carousel className="collection-carousel" setApi={setApi} opts={{align:'start',duration:0}} aria-label={collection.title} tabIndex={0}><div className="large-artwork"><CarouselContent>{collection.items.map((item,i)=><CarouselItem key={item.src} aria-label={`${i+1} of ${collection.items.length}`} aria-hidden={i!==selected}><Image unoptimized className="collection-art" src={item.src} width={item.width} height={item.height} alt={item.description+(item.totalViews>1?` — view ${item.view}`:'')} loading={i===0?'eager':'lazy'} draggable={false}/></CarouselItem>)}</CarouselContent></div><div className="painting-caption"><div aria-live="polite" aria-atomic="true"><h2>{current.title}</h2><p>{current.description}</p><span className="caption-note">Provisional title{current.totalViews>1?` · View ${current.view} of ${current.totalViews}`:''}</span></div><div className="sequence-controls"><button aria-label="Previous artwork" disabled={selected===0} onClick={()=>api?.scrollPrev()}>Previous</button><span>{String(selected+1).padStart(2,'0')} / {String(collection.items.length).padStart(2,'0')}</span><button aria-label="Next artwork" disabled={selected===collection.items.length-1} onClick={()=>api?.scrollNext()}>Next</button></div></div><fieldset className="thumbnail-row" ref={strip} aria-label="Choose an artwork">{collection.items.map((item,i)=><button key={item.src} ref={el=>{thumbs.current[i]=el}} className={'art-thumbnail'+(selected===i?' is-selected':'')} onClick={()=>api?.scrollTo(i)} aria-label={`${item.title}${item.totalViews>1?`, view ${item.view}`:''}`} aria-pressed={selected===i}><Image unoptimized src={item.src} width={item.width} height={item.height} alt="" loading="lazy"/><span>{String(i+1).padStart(2,'0')}</span></button>)}</fieldset></Carousel></section>
}
