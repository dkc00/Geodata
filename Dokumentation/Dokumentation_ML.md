- R^2 immer von Train und Test ausgeben. Eine sehr gute Performance auf Train, aber schlecht auf Test? Tendenziell Overfitting möglich 

- Immer zuerst die Datenqualität, Features und Feature Engineering priorisieren, dann ggfs Modelle durchtesten und Hyperparameter tunen.

- Simple Features wie bei Pegelvorhersage historische Pegelstände und Niederschläge? dann eher an features arbeiten als verschiedene modelle, zb RF, XGBoost, LightGBM.

- Bei Zeitreihen train/test niemals zufällig zuweisen, sondern immer ein gewisses split_date festlegen und entsprechend keine data leakage verursachen, also daten der zukunft ins training einspeisen. 

- Nicht "mehr features", sondern physikbasiert denken! welche features geben meinem modell zusätzliche information? Nur so viele Features wie nötig, sonst werden unnötige muster gelernt und es kommt zu overfitting. an das hautkrebs ml beispiel mit den linealen denken, oder Fotos von Zügen, bei denen das Modell die Gleise gelernt hat. 

- Varianz vs. Bias: An die Zielscheibe beim Bogenschießen denken. Nicht gezielt immer danebenschießen (Bias, wie bei der Geländevermessung mit Float-Signal), aber auch nicht random jedes Mal eine andere Stelle treffen (hohe Varianz, overfitting gefahr!) 

- von einer baseline aus modell aufbauen, zb erst auf pegelstand t trainieren, lagged features einbauen, dann auf t- t-1 (dt) trainieren, ggfs summen der niederschläge über 3 oder 7 tage als feature. was ist physikalisch sinnvoll?