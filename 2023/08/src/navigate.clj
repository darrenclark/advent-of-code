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

(defn count-until [f start {:keys [path nav-map]}]
  (reduce
   (fn [[curr n] dir]
     (if (f curr)
       (reduced n)
       [(left-or-right dir (nav-map curr)) (+ n 1)]))
   [start 0]
   (cycle path)))

(defn count-until-zzz [parsed]
  (count-until #(= "ZZZ" %1) "AAA" parsed))

(defn part1 [opts]
  {:pre [(contains? opts :input)]}
  (let [parsed (parse (opts :input))
        count (count-until-zzz parsed)]
    (println count)))

(defn count-until-ends-with-z [start parsed]
  (count-until #(str/ends-with? %1 "Z") start parsed))

(defn start-nodes [nav-map]
  (vec
   (filter #(str/ends-with? %1 "A") (keys nav-map))))

;; https://rosettacode.org/wiki/Least_common_multiple#Clojure
(defn gcd
  [a b]
  (if (zero? b)
    a
    (recur b, (mod a b))))
(defn lcm
  [a b]
  (/ (* a b) (gcd a b)))
(defn lcmv [& v] (reduce lcm v))

(defn part2 [opts]
  {:pre [(contains? opts :input)]}
  (let [parsed (parse (opts :input))
        starts (start-nodes (parsed :nav-map))
        counts (map #(count-until-ends-with-z %1 parsed) starts)
        result (apply lcmv counts)]
    (println result)))
