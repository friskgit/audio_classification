const slider = document.getElementById("waveSlider");
const sliderValue = document.getElementById("sliderValue");
const selectionVectorValue = document.getElementById("selectionVectorValue");
const nearestMatchValue = document.getElementById("nearestMatchValue");
const playClosestButton = document.getElementById("playClosestButton");
const playbackStatus = document.getElementById("playbackStatus");
const sineVector = [-472.2589416503906,45.31652069091797,28.601877212524414,14.050966262817383,-2.088310956954956,-17.738292694091797,-29.931062698364258,-37.01455307006836,-37.94674301147461,-32.679710388183594,-22.336088180541992,-8.806193351745605,5.653266906738281,18.52469825744629,27.87535858154297,32.273956298828125,31.281295776367188,25.336034774780273,15.678797721862793,4.0998759269714355,45.032588958740234,33.90424728393555,2.3489325046539307,1.1045430898666382,0.7559756636619568,0.8832541108131409,2.3915600776672363,3.4892070293426514,3.907639265060425,3.7290537357330322,2.7661654949188232,1.0673757791519165,0.6554727554321289,2.5849390029907227,3.8814961910247803,4.636447906494141,4.559037685394287,3.738025665283203,2.343632459640503,0.633693277835846,14.948949015358611,19.74732431315594,52.821987669252145,13.840254777719188,13.624181869868806,14.975760139974476,14.75018852666365,4.386941201602942,3.126673517406934,6.893188760867892,2.235856652738801,2.531933652426292,3.0303412475919496,3.359165560584858,0.35025691986083984,0.0161511842161417,0.039219647988505746];

const noiseVector = [44.63298797607422,-4.0250630378723145,-0.5988080501556396,-0.06168505921959877,-0.4449363648891449,0.3490011990070343,0.8350389003753662,0.5852862596511841,0.17441025376319885,0.3325101137161255,0.5236915349960327,-0.693240761756897,0.37950265407562256,0.0826677456498146,0.054992444813251495,0.17699865996837616,0.0992535799741745,-0.030659621581435204,0.2627945840358734,0.2866009473800659,6.233343124389648,2.610712766647339,2.7719836235046387,3.3304312229156494,2.5344629287719727,2.9204695224761963,2.6656134128570557,2.7090978622436523,2.6973838806152344,2.937561273574829,2.740466833114624,2.731961965560913,2.903578042984009,2.7073442935943604,3.605600357055664,3.3949687480926514,2.800252676010132,3.1934139728546143,2.915353536605835,2.510026216506958,10.667902381342751,9.894329901299207,12.05321548306998,12.040798727032596,12.933739840613192,13.351744300691724,13.287195862688888,3.081536389334999,2.7298135880227847,3.1012590703613605,2.04410784413359,1.5021683461298272,1.146435078810498,0.8706071847964758,0.19891464710235596,0.009862761944532394,0.4891455639367816];

let selectionVector = [];
let vectorDatabase = [];
let nearestMatch = null;
let currentNearestSoundFile = null;

const vectorFileNames = [
//  "reference-sine-220Hz-vector.json",
  "campione 1-vector.json",
  "campione 2-vector.json",
  "campione 3-vector.json",
  "campione 4-vector.json",
  "campione 5-vector.json",
  "campione 6-vector.json",
  "campione 7-vector.json",
  "campione 8-vector.json",
  "campione 9-vector.json",
  "campione 10-vector.json",
  "campione 11-vector.json",
  "campione 12-vector.json",
  "campione 13-vector.json",
  "campione 14-vector.json",
  "campione 15-vector.json",
  "campione 16-vector.json",
  "campione 17-vector.json",
  "campione 18-vector.json",
//  "reference-white-noise-vector.json",
];

const audioPlayer = new Audio();

const buildSelectionVector = (t) => {
  const length = Math.min(sineVector.length, noiseVector.length);
  return Array.from({ length }, (_, index) => {
    const sineValue = sineVector[index];
    const noiseValue = noiseVector[index];
    return sineValue + (noiseValue - sineValue) * t;
  });
};

const euclideanDistance = (a, b) => {
  const length = Math.min(a.length, b.length);
  let sum = 0;

  for (let index = 0; index < length; index += 1) {
    const delta = a[index] - b[index];
    sum += delta * delta;
  }

  return Math.sqrt(sum);
};

const findNearestMatch = () => {
  if (vectorDatabase.length === 0 || selectionVector.length === 0) {
    return null;
  }

  const candidates = vectorDatabase.map((entry) => ({
    ...entry,
    distance: euclideanDistance(selectionVector, entry.vector),
  }));

  candidates.sort((a, b) => a.distance - b.distance);
  return candidates[0];
};

const updateNearestMatchUI = () => {
  nearestMatch = findNearestMatch();

  if (!nearestMatch) {
    currentNearestSoundFile = null;
    nearestMatchValue.textContent = "Closest sound: unavailable";
    return false;
  }

  const hasChanged = currentNearestSoundFile !== nearestMatch.soundFile;
  currentNearestSoundFile = nearestMatch.soundFile;
  nearestMatchValue.textContent = `Closest sound: ${nearestMatch.soundFile} (distance: ${nearestMatch.distance.toFixed(2)})`;
  return hasChanged;
};

const loadVectorDatabase = async () => {
  try {
    const loadedVectors = await Promise.all(
      vectorFileNames.map(async (fileName) => {
        const response = await fetch(`Alberto/${encodeURIComponent(fileName)}`);
        if (!response.ok) {
          throw new Error(`Could not load ${fileName}`);
        }

        const data = await response.json();
        const soundFile = String(data[data.length - 1]);
        const vector = data.slice(0, -1).map((value) => Number(value));
        return { fileName, soundFile, vector };
      })
    );

    vectorDatabase = loadedVectors;
    updateNearestMatchUI();
  } catch (error) {
    nearestMatchValue.textContent = "Closest sound: failed to load vectors";
    playbackStatus.textContent = "Cannot play sounds until vectors are loaded.";
    console.error(error);
  }
};

const playClosest = async () => {
  if (!nearestMatch) {
    playbackStatus.textContent = "No closest sound available yet.";
    return;
  }

  try {
    audioPlayer.pause();
    audioPlayer.src = `Alberto/${encodeURIComponent(nearestMatch.soundFile)}`;
    audioPlayer.currentTime = 0;
    await audioPlayer.play();
    playbackStatus.textContent = `Playing ${nearestMatch.soundFile}...`;
  } catch (error) {
    playbackStatus.textContent = "Playback failed. Click the button again to retry.";
    console.error(error);
  }
};

const updateValue = (autoPlayOnChange = false) => {
  const mix = Number(slider.value);
  sliderValue.textContent = `Value: ${mix.toFixed(2)}`;
  selectionVector = buildSelectionVector(mix);
  const roundedSelectionVector = selectionVector.map((value) => Number(value.toFixed(2)));
  selectionVectorValue.textContent = `selectionVector: ${JSON.stringify(roundedSelectionVector)}`;
  const nearestChanged = updateNearestMatchUI();

  if (autoPlayOnChange && nearestChanged) {
    void playClosest();
  }
};

slider.addEventListener("input", () => {
  updateValue(true);
});
playClosestButton.addEventListener("click", () => {
  void playClosest();
});

updateValue();
void loadVectorDatabase();
