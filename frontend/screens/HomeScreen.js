import React, { useEffect, useState } from 'react';
import { FlatList, View, StyleSheet, ActivityIndicator, RefreshControl } from 'react-native';
import ExperienceCard from '../components/ExperienceCard';
import apiService from '../services/api';

export default function HomeScreen({ navigation, route }) {
  const [expList, setExpList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const loadExperiences = async () => {
    try {
      const experiences = await apiService.getExperiences();
      setExpList(experiences);
    } catch (error) {
      console.error('加载经验列表失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadExperiences();
    setRefreshing(false);
  };

  useEffect(() => {
    loadExperiences();
  }, []);

  useEffect(() => {
    if (route?.params?.newExperience) {
      setExpList(prev => [route.params.newExperience, ...prev]);
      // 清除参数，避免重复添加
      navigation.setParams({ newExperience: undefined });
    }
  }, [route?.params?.newExperience]);

  if (loading) {
    return (
      <View style={[styles.container, styles.centerContent]}>
        <ActivityIndicator size="large" color="#00C6AE" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <FlatList
        data={expList}
        keyExtractor={item => item.id.toString()}
        renderItem={({ item }) => (
          <ExperienceCard
            experience={item}
            onPress={() => navigation.navigate('经验详情', { experience: item })}
          />
        )}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F6F7FB', padding: 10 },
  centerContent: { justifyContent: 'center', alignItems: 'center' },
});
