import React, { useState } from 'react';
import { View, TextInput, FlatList, StyleSheet } from 'react-native';
import { experiences } from '../mock/experiences';
import ExperienceCard from '../components/ExperienceCard';

export default function SearchScreen({ navigation }) {
  const [query, setQuery] = useState('');
  const filtered = experiences.filter(
    exp =>
      exp.company.includes(query) ||
      exp.position.includes(query) ||
      exp.tags.some(tag => tag.includes(query))
  );
  return (
    <View style={styles.container}>
      <TextInput
        style={styles.input}
        placeholder="搜索公司/职位/标签"
        value={query}
        onChangeText={setQuery}
      />
      <FlatList
        data={filtered}
        keyExtractor={item => item.id.toString()}
        renderItem={({ item }) => (
          <ExperienceCard
            experience={item}
            onPress={() => navigation.navigate('经验详情', { experience: item })}
          />
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F6F7FB', padding: 10 },
  input: {
    backgroundColor: '#fff', borderRadius: 8, padding: 10, marginBottom: 10, fontSize: 16,
    borderColor: '#eee', borderWidth: 1,
  },
});
