(ns navigate
  (:require [clojure.string :as str]))

(defn parse-entry [entry]
  (let [no-punc (str/replace entry #"[(),]|= " "")
        parts (str/split no-punc #" ")]
    [(first parts) (vec (rest parts))]))

(defn parse [file-path]
  (let [lines (str/split (slurp file-path) #"\n")
        path-chars (seq (first lines))
        path (map str path-chars)
        entries (map parse-entry (drop 2 lines))]
    {:path path
     :nav-map (into {} entries)}))

(defn left-or-right [side [left right]]
  (if (= side "L") left right))

(defn count-until-zzz [{:keys [path nav-map]}]
  (reduce
    (fn [[curr n] dir]
      (if (= curr "ZZZ")
        (reduced n)
        [(left-or-right dir (nav-map curr)) (+ n 1)]))
    ["AAA" 0]
    (cycle path)))

(defn part1 [opts]
  {:pre [(contains? opts :input)]}
  (let [parsed (parse (opts :input))
        count (count-until-zzz parsed)]
    (println count)))
