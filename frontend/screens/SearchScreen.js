import React, { useState, useEffect } from 'react';
import { View, TextInput, FlatList, StyleSheet, ActivityIndicator } from 'react-native';
import ExperienceCard from '../components/ExperienceCard';
import apiService from '../services/api';

export default function SearchScreen({ navigation }) {
  const [query, setQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const performSearch = async (searchQuery) => {
    if (!searchQuery.trim()) {
      setSearchResults([]);
      return;
    }

    setLoading(true);
    try {
      const results = await apiService.searchExperiences(searchQuery);
      setSearchResults(results);
    } catch (error) {
      console.error('搜索失败:', error);
      setSearchResults([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const timeoutId = setTimeout(() => {
      performSearch(query);
    }, 500); // 防抖延迟

    return () => clearTimeout(timeoutId);
  }, [query]);
  return (
    <View style={styles.container}>
      <TextInput
        style={styles.input}
        placeholder="搜索公司/职位/标签"
        value={query}
        onChangeText={setQuery}
      />
      {loading && (
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#00C6AE" />
        </View>
      )}
      <FlatList
        data={searchResults}
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
  loadingContainer: {
    position: 'absolute',
    top: 60,
    left: 0,
    right: 0,
    alignItems: 'center',
    zIndex: 1,
  },
});
