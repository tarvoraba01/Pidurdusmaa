/* Struktuurandmed (schema.org JSON-LD), mida mitu lehte jagab.
   Organisatsioon ja veebisait on avalehel; tööriistalehed viitavad neile
   @id kaudu, nii et Google seob need üheks üksuseks. */
export const BASE = 'https://pidurdusmaa.ee';
export const ORG_ID = BASE + '/#org';
export const SITE_ID = BASE + '/#website';

export const ORG = {
	'@type': 'Organization',
	'@id': ORG_ID,
	name: 'Pidurdusmaa.ee',
	url: BASE + '/',
	logo: { '@type': 'ImageObject', url: BASE + '/apple-touch-icon.png', width: 180, height: 180 },
	contactPoint: {
		'@type': 'ContactPoint',
		contactType: 'customer support',
		url: BASE + '/kontakt/',
		availableLanguage: ['et']
	}
};

export const WEBSITE = {
	'@type': 'WebSite',
	'@id': SITE_ID,
	url: BASE + '/',
	name: 'Pidurdusmaa.ee',
	inLanguage: 'et',
	publisher: { '@id': ORG_ID }
};

/** Veebitööriist (kalkulaator, rehvi valimine, võrdlus). */
export function tooriist(name, path, description) {
	return {
		'@type': 'WebApplication',
		'@id': BASE + path + '#tooriist',
		name,
		url: BASE + path,
		description,
		applicationCategory: 'UtilitiesApplication',
		operatingSystem: 'Any',
		browserRequirements: 'Vajab JavaScripti',
		inLanguage: 'et',
		isAccessibleForFree: true,
		offers: { '@type': 'Offer', price: '0', priceCurrency: 'EUR' },
		publisher: { '@id': ORG_ID }
	};
}

import { AUTOR_NIMI } from './seaded.js';

/** Artikli autor: inimene, kui nimi on seadetes, muidu organisatsioon. */
export const AUTOR_ID = BASE + '/meist/#autor';
export const AUTOR = AUTOR_NIMI
	? { '@type': 'Person', '@id': AUTOR_ID, name: AUTOR_NIMI, url: BASE + '/meist/', worksFor: { '@id': ORG_ID } }
	: null;
export const autorRef = () => (AUTOR ? { '@id': AUTOR_ID } : { '@id': ORG_ID });

/** Artikli JSON-LD (Article + autor), ühine kõigile Teadmine-lehtedele. */
export function artikkel({ path, title, desc, uuendatud, avaldatud }) {
	return [
		{
			'@type': 'Article',
			'@id': BASE + path + '#artikkel',
			headline: title,
			description: desc,
			inLanguage: 'et',
			datePublished: avaldatud || uuendatud,
			dateModified: uuendatud,
			author: autorRef(),
			publisher: { '@id': ORG_ID },
			mainEntityOfPage: BASE + path,
			image: BASE + '/og/sait/avaleht.png'
		},
		...(AUTOR ? [AUTOR] : []),
		ORG
	];
}

export const graph = (...items) => ({ '@context': 'https://schema.org', '@graph': items });
