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

export const graph = (...items) => ({ '@context': 'https://schema.org', '@graph': items });
