import { useCallback, useEffect, useState } from 'react';
import { FlatList, RefreshControl, StyleSheet, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Avatar } from '@/components/ui/avatar';
import { EmptyState } from '@/components/ui/empty-state';
import { ListItem } from '@/components/ui/list-item';
import { Text } from '@/components/ui/text';
import { Radius, Spacing } from '@/constants/theme';
import { useTheme } from '@/hooks/use-theme';
import { listConversations, type Conversation } from '@/services/messages';

export default function MessagesScreen() {
  const { colors } = useTheme();
  const [items, setItems] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    listConversations()
      .then(setItems)
      .finally(() => setLoading(false));
  }, []);

  const refresh = useCallback(async () => {
    setRefreshing(true);
    try {
      setItems(await listConversations());
    } finally {
      setRefreshing(false);
    }
  }, []);

  return (
    <SafeAreaView edges={['top']} style={[styles.flex, { backgroundColor: colors.background }]}>
      <Text variant="title" accessibilityRole="header" style={styles.title}>
        Messages
      </Text>
      <FlatList
        data={items}
        keyExtractor={(item) => item.id}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={refresh} tintColor={colors.primary} />}
        ItemSeparatorComponent={() => <View style={[styles.separator, { backgroundColor: colors.border }]} />}
        ListEmptyComponent={
          loading ? undefined : <EmptyState icon="chatbubbles-outline" title="Aucun message" message="Vos conversations apparaîtront ici." />
        }
        contentContainerStyle={items.length ? undefined : styles.flex}
        renderItem={({ item }) => (
          <ListItem
            title={item.name}
            subtitle={item.lastMessage}
            left={<Avatar name={item.name} />}
            right={
              <View style={styles.meta}>
                <Text variant="caption" color={item.unread ? 'primaryText' : 'textMuted'}>
                  {item.time}
                </Text>
                {item.unread ? (
                  <View style={[styles.badge, { backgroundColor: colors.primary }]} accessibilityLabel={`${item.unread} non lus`}>
                    <Text variant="caption" style={{ color: colors.onPrimary, fontWeight: '700' }}>
                      {item.unread}
                    </Text>
                  </View>
                ) : null}
              </View>
            }
            onPress={() => {}}
          />
        )}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  flex: { flex: 1 },
  title: { paddingHorizontal: Spacing.xl, paddingTop: Spacing.lg, paddingBottom: Spacing.sm },
  separator: { height: StyleSheet.hairlineWidth, marginLeft: 76 },
  meta: { alignItems: 'flex-end', gap: Spacing.xs },
  badge: { minWidth: 20, height: 20, borderRadius: Radius.pill, alignItems: 'center', justifyContent: 'center', paddingHorizontal: 6 },
});
