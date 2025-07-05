import React from 'react';
import { View, Text, ScrollView, StyleSheet } from 'react-native';

export default function ExperienceDetailScreen({ route }) {
  const { experience } = route.params;
  return (
    <ScrollView style={styles.container}>
      <Text style={styles.company}>{experience.company}</Text>
      <Text style={styles.position}>{experience.position}</Text>
      <View style={styles.tags}>
        {experience.tags.map(tag => (
          <Text key={tag} style={styles.tag}>{tag}</Text>
        ))}
      </View>
      <Text style={styles.summary}>{experience.summary}</Text>
      <Text style={styles.content}>{experience.content}</Text>
      <View style={styles.footer}>
        <Text style={styles.user}>{experience.user.username}</Text>
        <Text style={styles.time}>{experience.created_at}</Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff', padding: 16 },
  company: { fontWeight: 'bold', fontSize: 20, color: '#222' },
  position: { color: '#00C6AE', fontSize: 16, marginTop: 2 },
  tags: { flexDirection: 'row', marginTop: 8, flexWrap: 'wrap' },
  tag: { backgroundColor: '#E6F7F4', color: '#00C6AE', borderRadius: 6, paddingHorizontal: 8, marginRight: 6, fontSize: 12 },
  summary: { color: '#333', marginTop: 12, fontWeight: 'bold' },
  content: { color: '#444', marginTop: 12, lineHeight: 22 },
  footer: { flexDirection: 'row', justifyContent: 'space-between', marginTop: 20 },
  user: { color: '#888', fontSize: 12 },
  time: { color: '#aaa', fontSize: 12 },
});
