// File: components/ThemeRegistry/EmotionCache.tsx
'use client';
import * as React from 'react';
import { CacheProvider } from '@emotion/react';
import createCache from '@emotion/cache';
import { useServerInsertedHTML } from 'next/navigation';

// This implementation is directly from MUI's documentation for the Next.js App Router.
// It ensures that MUI's styles are correctly handled on the server and client.
export default function NextAppDirEmotionCacheProvider(props: { options: any; children: React.ReactNode }) {
    const { options, children } = props;

    const [{ cache, flush }] = React.useState(() => {
        // Create an Emotion cache instance with the provided options.
        const cache = createCache(options);
        cache.compat = true;
        const prevInsert = cache.insert;
        let inserted: string[] = [];

        // We override the 'insert' method to keep track of styles inserted during SSR.
        cache.insert = (...args) => {
            const serialized = args[1];
            // @ts-ignore
            if (cache.inserted[serialized] === undefined) {
                // @ts-ignore
                inserted.push(serialized);
            }
            return prevInsert(...args);
        };

        // The 'flush' function returns the collected styles and clears the array.
        const flush = () => {
            const prevInserted = inserted;
            inserted = [];
            return prevInserted;
        };
        return { cache, flush };
    });

    // This hook from Next.js is used to inject the server-side rendered styles
    // into the <head> of the HTML document.
    useServerInsertedHTML(() => {
        const inserted = flush();
        if (inserted.length === 0) {
            return null;
        }
        return (
            <style
                data-emotion={`${cache.key} ${inserted.join(' ')}`}
                dangerouslySetInnerHTML={{
                    __html: inserted.join(''),
                }}
            />
        );
    });

    // On the client side, we wrap the children with Emotion's CacheProvider.
    return <CacheProvider value={cache}>{children}</CacheProvider>;
}

