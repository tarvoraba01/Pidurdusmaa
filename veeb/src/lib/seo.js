/* Lehe pealkiri ja kirjeldus ühest kohast — sama roll, mis oli inc/seo.php-l. */
export const SAIT = 'Pidurdusmaa.ee';
export const BASE = 'https://pidurdusmaa.ee';

export function titleFor(t) {
  return t ? t + ' | ' + SAIT : SAIT + ' — kui kiiresti sinu auto peatub?';
}
