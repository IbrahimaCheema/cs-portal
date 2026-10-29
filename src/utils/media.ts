// Hybrid Media Resolver: Local-First during Staging, Cloudflare R2 Ready for Production Cutover
const USE_R2 = import.meta.env.PUBLIC_MEDIA_MODE === 'r2';
const R2_DOMAIN = import.meta.env.PUBLIC_R2_DOMAIN || 'https://docs.crescentschool.edu.pk';

export function getMediaUrl(path: string): string {
  if (!path) return '';
  if (path.startsWith('http://') || path.startsWith('https://')) return path;
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  return USE_R2 ? `${R2_DOMAIN}${cleanPath}` : cleanPath;
}
