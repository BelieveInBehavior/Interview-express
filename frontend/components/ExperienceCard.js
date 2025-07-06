import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';

export default function ExperienceCard({ experience, onPress }) {
  return (
    <TouchableOpacity style={styles.card} onPress={onPress}>
      <View style={{ flexDirection: 'row', justifyContent: 'space-between' }}>
        <Text style={styles.company}>{experience.company}</Text>
        <Text style={styles.difficulty}>难度: {experience.difficulty}/5</Text>
      </View>
      <Text style={styles.position}>{experience.position}</Text>
      <Text style={styles.summary} numberOfLines={2}>{experience.summary}</Text>
      <View style={styles.tags}>
        {experience.tags.map(tag => (
          <Text key={tag} style={styles.tag}>{tag}</Text>
        ))}
      </View>
      <View style={styles.footer}>
        <Text style={styles.user}>{experience.user?.username || "匿名用户"}</Text>
        <Text style={styles.time}>{experience.created_at}</Text>
      </View>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#fff', borderRadius: 12, padding: 16, marginBottom: 12,
    shadowColor: '#000', shadowOpacity: 0.05, shadowRadius: 8, elevation: 2,
  },
  company: { fontWeight: 'bold', fontSize: 16, color: '#222' },
  difficulty: { color: '#00C6AE', fontWeight: 'bold' },
  position: { color: '#555', marginTop: 2 },
  summary: { color: '#333', marginTop: 8 },
  tags: { flexDirection: 'row', marginTop: 8, flexWrap: 'wrap' },
  tag: { backgroundColor: '#E6F7F4', color: '#00C6AE', borderRadius: 6, paddingHorizontal: 8, marginRight: 6, fontSize: 12 },
  footer: { flexDirection: 'row', justifyContent: 'space-between', marginTop: 10 },
  user: { color: '#888', fontSize: 12 },
  time: { color: '#aaa', fontSize: 12 },
});
