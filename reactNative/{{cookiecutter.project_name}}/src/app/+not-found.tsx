import { Link } from 'expo-router';
import { EmptyState } from '@/components/ui/empty-state';
import { Screen } from '@/components/ui/screen';
import { Button } from '@/components/ui/button';

export default function NotFound() {
  return (
    <Screen scroll={false}>
      <EmptyState icon="compass-outline" title="Page introuvable" message="Ce lien ne mène nulle part." />
      <Link href="/" asChild>
        <Button title="Retour à l'accueil" variant="secondary" />
      </Link>
    </Screen>
  );
}
