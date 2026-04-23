import {useState, useEffect} from 'react';
import {ActivityIndicator, ScrollView, View, Text, StyleSheet, Pressable} from 'react-native';
import {SafeAreaView, SafeAreaProvider} from 'react-native-safe-area-context';

export default function SavedScreen() {
  const [savedSpots, setSavedSpots] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(false); //update after fixing backend for fetch
  }, []);

  if (loading) return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <ActivityIndicator />
    </View>
  );

  return (
    
        <View style={styles.screen}>
          {savedSpots.length > 0 ? (
            <ScrollView>
              {/* {savedSpots.map(spot => (
                <StudySpotCard key={spot.id} spot={spot} />
              ))} */}
            </ScrollView>
          ) : (
            
            <View style={{flex : 1}}>
              <SavedStudySpots />
              <TextButton onPress={() => console.log("Explore pressed")} />
            </View>
          )}
        </View>
  );
}

const SavedStudySpots = () => {
  return (
    <Text style={styles.savedStudySpots}>Saved Study Spots</Text>
  );
}

type TextButtonProps = {
  onPress?: () => void;
};

const TextButton: React.FC<TextButtonProps> = ({onPress}) => {
  return (
    <View style={styles.container}>
      <View style={styles.textContainer}>
        <Text style={[styles.title, styles.mediumText]}>
          No saved study spots yet!
        </Text>

        <Text style={styles.subtitle}>To keep track of spots you like,</Text>
<Text style={styles.subtitle}>bookmark them for later.</Text>
      </View>

      <Pressable style={styles.buttonContainer} onPress={onPress}>
        <Text style={[styles.buttonText, styles.mediumText]}>
          Explore Study Spots
        </Text>
      </Pressable>
    </View>
  );
};

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: "#fff",
    padding: 16,
  },

  savedStudySpots: {
    fontSize: 26,
    fontWeight: "700",
    fontFamily: "Roboto Flex",
    color: "#000",
    textAlign: "left"
  },

  mediumText: {
    fontFamily: "Roboto Flex",
    fontWeight: "500",
    textAlign: "center",
  },

  container: {
    width: "100%",
    flex: 1,
    alignItems: "center",
    justifyContent: "center"
  },

  textContainer: {
    alignSelf: "stretch",
    marginBottom: 16, // replaces gap
  },

  title: {
    fontSize: 18,
    color: "#000",
    textAlign: "center",
    marginBottom: 8,
  },

  subtitle: {
    fontSize: 16,
    letterSpacing: 0.3,
    fontFamily: "RobotoFlex-Regular",
    color: "#94a3b8",
      textAlign: "center",
  },


  buttonContainer: {
    borderRadius: 8,
    backgroundColor: "#bf5700",
    flexDirection: "row",
    justifyContent: "center",
    paddingHorizontal: 16,
    paddingVertical: 12,
    alignItems: "center",
  },

  buttonText: {
    fontSize: 14,
    color: "#f9fafb",
    textAlign: "center",
  },
});

