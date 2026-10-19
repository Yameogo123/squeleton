/** Placeholder data source for the Messages tab: replace with real API calls. */
export type Conversation = { id: string; name: string; lastMessage: string; time: string; unread: number };

export async function listConversations(): Promise<Conversation[]> {
  return [
    { id: '1', name: 'Équipe support', lastMessage: 'Bienvenue ! Comment pouvons-nous aider ?', time: '09:41', unread: 2 },
    { id: '2', name: 'Awa Traoré', lastMessage: 'Le document est prêt.', time: 'Hier', unread: 0 },
    { id: '3', name: 'Moussa Diallo', lastMessage: 'Merci pour ton retour 🙏', time: 'Lun.', unread: 0 },
  ];
}
