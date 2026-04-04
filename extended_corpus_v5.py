"""
extended_corpus_v5.py
-----------------------
Extended educational documents corpus (version 5).
Exports: EXTENDED_DOCUMENTS_V5
"""

EXTENDED_DOCUMENTS_V5 = [   {   'grade': '9',
        'subject': 'mathematics',
        'text': 'Trigonometry studies the relationships between the angles and sides of triangles. The three main '
                'trigonometric ratios are sine, cosine, and tangent, which compare pairs of sides in a right-angled '
                'triangle. These ratios are used to find unknown sides or angles when some measurements are already '
                'known.',
        'topic': 'trigonometry'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'The memory aid SOH CAH TOA helps recall the three trigonometric ratios. SOH means sine equals '
                'opposite over hypotenuse, CAH means cosine equals adjacent over hypotenuse, and TOA means tangent '
                'equals opposite over adjacent. The hypotenuse is always the longest side, opposite the right angle.',
        'topic': 'trigonometry'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'To find a missing side in a right triangle, choose the correct ratio and set up an equation. For '
                'example, if a triangle has an angle of 30 degrees and the hypotenuse is 10 cm, the opposite side '
                'equals sine of 30 degrees times 10, which is 0.5 times 10, giving 5 cm. Always identify which sides '
                'are opposite, adjacent, and hypotenuse relative to the angle you are using.',
        'topic': 'trigonometry'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'The Pythagorean theorem states that a squared plus b squared equals c squared, where c is the '
                'hypotenuse of a right-angled triangle. For example, if a equals 3 and b equals 4, then c squared '
                'equals 9 plus 16 equals 25, so c equals 5. This theorem only applies to right-angled triangles.',
        'topic': 'trigonometry'},
    {   'grade': '10',
        'subject': 'mathematics',
        'text': 'Angles can be measured in degrees or radians. A full circle is 360 degrees or 2 pi radians, and a '
                'straight line is 180 degrees or pi radians. To convert degrees to radians, multiply by pi divided by '
                '180; to convert radians to degrees, multiply by 180 divided by pi.',
        'topic': 'trigonometry'},
    {   'grade': '10',
        'subject': 'mathematics',
        'text': 'The unit circle is a circle with radius 1 centred at the origin of a coordinate plane. For any angle '
                'theta measured from the positive x-axis, the x-coordinate of the point on the circle equals cosine '
                'theta and the y-coordinate equals sine theta. This definition extends trigonometry beyond right '
                'triangles to all angles.',
        'topic': 'trigonometry'},
    {   'grade': '10',
        'subject': 'mathematics',
        'text': 'Inverse trigonometric functions are used to find an angle when a ratio is known. For instance, if '
                'sine of an angle equals 0.6, then the angle equals arcsin of 0.6, which is approximately 36.87 '
                'degrees. The inverse functions are written as arcsin, arccos, and arctan, or sometimes as sin to the '
                'power of negative one.',
        'topic': 'trigonometry'},
    {   'grade': '10',
        'subject': 'mathematics',
        'text': 'The graphs of sine and cosine are smooth, repeating waves. The sine function starts at zero, rises to '
                'a maximum of 1 at 90 degrees, returns to zero at 180 degrees, dips to negative 1 at 270 degrees, and '
                'completes one full cycle at 360 degrees. The cosine graph has the same shape but is shifted 90 '
                'degrees to the left compared to sine.',
        'topic': 'trigonometry'},
    {   'grade': '11',
        'subject': 'mathematics',
        'text': 'Trigonometric identities are equations that are true for all values of the variable. The most '
                'fundamental is the Pythagorean identity: sine squared theta plus cosine squared theta equals 1. This '
                'identity can be rearranged to give sine squared theta equals 1 minus cosine squared theta, which is '
                'useful for simplifying expressions.',
        'topic': 'trigonometry'},
    {   'grade': '11',
        'subject': 'mathematics',
        'text': 'The double angle formulae state that sine of 2A equals 2 sine A cosine A, and cosine of 2A equals '
                'cosine squared A minus sine squared A. These are derived from the compound angle formulae and are '
                'often used to simplify integrals and solve equations. For example, sine of 60 degrees equals 2 sine '
                '30 degrees cosine 30 degrees equals 2 times 0.5 times root 3 over 2 equals root 3 over 2.',
        'topic': 'trigonometry'},
    {   'grade': '11',
        'subject': 'mathematics',
        'text': 'The sine rule states that a divided by sine A equals b divided by sine B equals c divided by sine C, '
                'where a, b, c are the side lengths opposite to angles A, B, C respectively. It is used to solve '
                'non-right triangles when you know two angles and one side, or two sides and a non-included angle. For '
                'example, if a equals 7, A equals 40 degrees, and B equals 60 degrees, then b equals 7 times sine 60 '
                'divided by sine 40, which is approximately 9.39.',
        'topic': 'trigonometry'},
    {   'grade': '11',
        'subject': 'mathematics',
        'text': 'The cosine rule states that c squared equals a squared plus b squared minus 2ab cosine C, where C is '
                'the included angle between sides a and b. It generalises the Pythagorean theorem for any triangle. '
                'When C equals 90 degrees, cosine C equals 0 and the formula reduces to c squared equals a squared '
                'plus b squared.',
        'topic': 'trigonometry'},
    {   'grade': '12',
        'subject': 'mathematics',
        'text': 'Trigonometric equations can have multiple solutions because trig functions are periodic. For example, '
                'sine theta equals 0.5 gives theta equals 30 degrees as a principal value, but also 150 degrees in the '
                'range 0 to 360 degrees, and infinitely many solutions beyond. The general solution for sine theta '
                'equals sine alpha is theta equals n times 180 degrees plus or minus alpha, adjusted for the period of '
                'the function.',
        'topic': 'trigonometry'},
    {   'grade': '12',
        'subject': 'mathematics',
        'text': 'Trigonometry is applied in navigation, engineering, and physics. For example, to find the height of a '
                'building, you measure the angle of elevation from a known distance. If you stand 50 metres from the '
                'base and the angle of elevation is 62 degrees, then the height equals 50 times tangent of 62 degrees, '
                'which is approximately 94 metres.',
        'topic': 'trigonometry'},
    {   'grade': '12',
        'subject': 'mathematics',
        'text': 'The reciprocal trigonometric functions are cosecant, secant, and cotangent. Cosecant theta equals 1 '
                'divided by sine theta, secant theta equals 1 divided by cosine theta, and cotangent theta equals 1 '
                'divided by tangent theta. These appear frequently in advanced calculus and physics, particularly in '
                'integration and wave mechanics.',
        'topic': 'trigonometry'},
    {   'grade': '7',
        'subject': 'mathematics',
        'text': 'A variable is a letter that represents an unknown number in mathematics. Expressions such as 3x plus '
                '5 combine variables and numbers using operations but have no equals sign. Equations, on the other '
                'hand, have an equals sign and state that two expressions are equal, for example 3x plus 5 equals 14.',
        'topic': 'algebra'},
    {   'grade': '7',
        'subject': 'mathematics',
        'text': 'To solve a simple linear equation, perform the same operation on both sides to isolate the variable. '
                'For example, to solve 2x plus 3 equals 11, first subtract 3 from both sides to get 2x equals 8, then '
                'divide both sides by 2 to get x equals 4. Always check your answer by substituting back into the '
                'original equation.',
        'topic': 'algebra'},
    {   'grade': '7',
        'subject': 'mathematics',
        'text': 'Substitution means replacing a variable with a given number to evaluate an expression. If a equals 3 '
                'and b equals 5, then the expression 2a plus b equals 2 times 3 plus 5 equals 6 plus 5 equals 11. '
                'Substitution is used to check solutions and evaluate formulas.',
        'topic': 'algebra'},
    {   'grade': '7',
        'subject': 'mathematics',
        'text': 'Expanding brackets means multiplying each term inside the bracket by the term outside. For example, 3 '
                'times open bracket 2x plus 4 close bracket equals 6x plus 12. When two brackets are multiplied '
                'together, each term in the first bracket multiplies every term in the second, which is sometimes '
                'called the FOIL method.',
        'topic': 'algebra'},
    {   'grade': '7',
        'subject': 'mathematics',
        'text': 'A sequence is an ordered list of numbers that follow a rule or pattern. An arithmetic sequence '
                'increases or decreases by a fixed amount called the common difference. For example, 3, 7, 11, 15 is '
                'an arithmetic sequence with a common difference of 4.',
        'topic': 'algebra'},
    {   'grade': '8',
        'subject': 'mathematics',
        'text': 'Factorisation is the reverse of expanding brackets; it means writing an expression as a product of '
                'its factors. For example, 6x plus 9 can be factorised as 3 times open bracket 2x plus 3 close '
                'bracket, because 3 is the highest common factor of both terms. Factorisation is a key skill for '
                'simplifying expressions and solving equations.',
        'topic': 'algebra'},
    {   'grade': '8',
        'subject': 'mathematics',
        'text': 'Simultaneous equations are two or more equations that share the same variables and must be solved '
                'together. The substitution method involves rearranging one equation to express one variable in terms '
                'of the other, then substituting into the second equation. For example, if x plus y equals 10 and x '
                'minus y equals 2, adding the equations gives 2x equals 12, so x equals 6 and y equals 4.',
        'topic': 'algebra'},
    {   'grade': '8',
        'subject': 'mathematics',
        'text': 'An inequality shows that one expression is greater than or less than another. For example, 2x plus 1 '
                'is greater than 7 means 2x is greater than 6, so x is greater than 3. When multiplying or dividing '
                'both sides of an inequality by a negative number, the inequality sign must be reversed.',
        'topic': 'algebra'},
    {   'grade': '8',
        'subject': 'mathematics',
        'text': 'The nth term formula for an arithmetic sequence is a plus open bracket n minus 1 close bracket times '
                'd, where a is the first term and d is the common difference. For the sequence 5, 8, 11, 14, a equals '
                '5 and d equals 3, so the nth term is 5 plus 3 times open bracket n minus 1 close bracket, which '
                'simplifies to 3n plus 2. The 10th term would be 3 times 10 plus 2 equals 32.',
        'topic': 'algebra'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'A quadratic equation has the form ax squared plus bx plus c equals 0, where a is not zero. Quadratics '
                'can be solved by factorising when the expression factors neatly. For example, x squared plus 5x plus '
                '6 equals 0 factorises to open bracket x plus 2 close bracket times open bracket x plus 3 close '
                'bracket equals 0, giving solutions x equals negative 2 or x equals negative 3.',
        'topic': 'algebra'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'The quadratic formula gives the solutions to any quadratic equation ax squared plus bx plus c equals '
                '0. The formula is x equals negative b plus or minus the square root of open bracket b squared minus '
                '4ac close bracket, all divided by 2a. The expression b squared minus 4ac is called the discriminant; '
                'if it is positive there are two solutions, if zero there is one, and if negative there are no real '
                'solutions.',
        'topic': 'algebra'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'Completing the square rewrites a quadratic in the form open bracket x plus p close bracket squared '
                'plus q. For x squared plus 6x plus 5, halve the coefficient of x to get 3, then write open bracket x '
                'plus 3 close bracket squared minus 9 plus 5, which simplifies to open bracket x plus 3 close bracket '
                'squared minus 4. This method reveals the vertex of a parabola at the point negative 3, negative 4.',
        'topic': 'algebra'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'The elimination method for simultaneous equations involves adding or subtracting the equations to '
                'remove one variable. For 3x plus 2y equals 16 and 3x minus y equals 7, subtracting the second from '
                'the first gives 3y equals 9, so y equals 3. Substituting back gives x equals 10 thirds, approximately '
                '3.33.',
        'topic': 'algebra'},
    {   'grade': '10',
        'subject': 'mathematics',
        'text': 'Algebraic fractions can be simplified by factorising the numerator and denominator and cancelling '
                'common factors. For example, open bracket x squared minus 4 close bracket divided by open bracket x '
                'minus 2 close bracket equals open bracket x plus 2 close bracket times open bracket x minus 2 close '
                'bracket divided by open bracket x minus 2 close bracket, which simplifies to x plus 2, provided x is '
                'not equal to 2. This process is similar to simplifying numerical fractions.',
        'topic': 'algebra'},
    {   'grade': '10',
        'subject': 'mathematics',
        'text': 'Rearranging a formula means making a different variable the subject. In the formula v equals u plus '
                'at, to make t the subject, subtract u from both sides to get v minus u equals at, then divide by a to '
                'get t equals open bracket v minus u close bracket divided by a. This skill is essential in science '
                'and engineering where the same formula is used in different contexts.',
        'topic': 'algebra'},
    {   'grade': '8',
        'subject': 'mathematics',
        'text': 'The mean of a data set is found by adding all the values and dividing by how many values there are. '
                'For the data set 4, 7, 9, 10, 10, the sum is 40 and there are 5 values, so the mean is 40 divided by '
                '5 equals 8. The mean is the most commonly used average but is sensitive to extreme values called '
                'outliers.',
        'topic': 'statistics'},
    {   'grade': '8',
        'subject': 'mathematics',
        'text': 'The median is the middle value when data is arranged in order. For the data 3, 5, 7, 9, 11, the '
                'median is 7. If there is an even number of values, the median is the mean of the two middle values. '
                'The median is more suitable than the mean when data contains outliers, as it is not affected by '
                'extreme values.',
        'topic': 'statistics'},
    {   'grade': '8',
        'subject': 'mathematics',
        'text': 'The mode is the value that appears most often in a data set. In the data 2, 4, 4, 5, 7, 4, 9, the '
                'mode is 4 because it appears three times. A data set can have more than one mode if two values appear '
                'equally often, and it is described as bimodal. The mode is the only average that can be used with '
                'non-numerical data such as colours or categories.',
        'topic': 'statistics'},
    {   'grade': '8',
        'subject': 'mathematics',
        'text': 'The range of a data set is the difference between the largest and smallest values. For the data 12, '
                '5, 19, 8, 15, the range is 19 minus 5 equals 14. The range gives a simple measure of the spread of '
                'data, but it is affected by outliers. A large range means the data is more spread out.',
        'topic': 'statistics'},
    {   'grade': '8',
        'subject': 'mathematics',
        'text': 'A frequency table organises data by listing each value or group and how many times it occurs. Grouped '
                'frequency tables use class intervals such as 0 to 9, 10 to 19, and so on, when data covers a wide '
                'range. The frequency of each class is the count of data values that fall within that interval.',
        'topic': 'statistics'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'A histogram displays grouped continuous data as bars, where the area of each bar represents the '
                'frequency. Unlike bar charts, there are no gaps between the bars and the horizontal axis shows a '
                'continuous scale. When class intervals are equal, the height of each bar equals the frequency; when '
                'intervals differ, the height equals the frequency density, which is frequency divided by class width.',
        'topic': 'statistics'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'A box plot, also called a box-and-whisker diagram, displays the minimum, lower quartile, median, '
                'upper quartile, and maximum of a data set. The interquartile range is the upper quartile minus the '
                'lower quartile and represents the spread of the middle 50 percent of the data. Box plots are '
                'particularly useful for comparing two distributions side by side.',
        'topic': 'statistics'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'A scatter graph plots two variables against each other to investigate whether a relationship exists. '
                'If the points broadly follow an upward trend, there is positive correlation; a downward trend '
                'indicates negative correlation. A line of best fit, also called a regression line, is drawn through '
                'the middle of the points and can be used to make predictions.',
        'topic': 'statistics'},
    {   'grade': '10',
        'subject': 'mathematics',
        'text': 'Correlation measures the strength and direction of a linear relationship between two variables. A '
                'correlation of positive 1 indicates perfect positive correlation, zero indicates no linear '
                'relationship, and negative 1 indicates perfect negative correlation. It is important to remember that '
                'correlation does not imply causation; a third variable may be responsible for the observed '
                'relationship.',
        'topic': 'statistics'},
    {   'grade': '10',
        'subject': 'mathematics',
        'text': 'Standard deviation measures how spread out values are around the mean. A small standard deviation '
                'means values are clustered close to the mean, while a large standard deviation indicates they are '
                'widely spread. The formula for population standard deviation is the square root of the mean of the '
                'squared deviations from the mean.',
        'topic': 'statistics'},
    {   'grade': '10',
        'subject': 'mathematics',
        'text': 'Sampling is the process of selecting a subset of a population to draw conclusions about the whole. A '
                'random sample gives every member of the population an equal chance of being selected and reduces '
                'bias. Stratified sampling divides the population into groups and selects members from each group in '
                'proportion to the group size.',
        'topic': 'statistics'},
    {   'grade': '10',
        'subject': 'mathematics',
        'text': 'Bias in statistics occurs when a sample does not accurately represent the population. For example, '
                'surveying only students in one class about school canteen preferences would give biased results '
                'because it excludes students with different preferences. Identifying and minimising bias is essential '
                'when collecting data for statistical investigations.',
        'topic': 'statistics'},
    {   'grade': '11',
        'subject': 'mathematics',
        'text': 'The normal distribution is a bell-shaped, symmetric distribution described by its mean and standard '
                'deviation. In a normal distribution, approximately 68 percent of data falls within one standard '
                'deviation of the mean, about 95 percent within two standard deviations, and about 99.7 percent within '
                'three. This is known as the empirical rule or 68-95-99.7 rule.',
        'topic': 'statistics'},
    {   'grade': '11',
        'subject': 'mathematics',
        'text': 'A cumulative frequency graph is drawn by plotting the running total of frequencies against the upper '
                'class boundary. The median can be read from the cumulative frequency graph at the point where the '
                'cumulative frequency equals half the total frequency. Quartiles are found at one quarter and three '
                'quarters of the total frequency.',
        'topic': 'statistics'},
    {   'grade': '6',
        'subject': 'mathematics',
        'text': 'Angles on a straight line add up to 180 degrees. Angles around a point add up to 360 degrees. '
                'Vertically opposite angles are equal and are formed when two straight lines cross each other.',
        'topic': 'geometry'},
    {   'grade': '6',
        'subject': 'mathematics',
        'text': 'A triangle has three sides and three angles that always add up to 180 degrees. An equilateral '
                'triangle has all three sides equal and all angles equal to 60 degrees. An isosceles triangle has two '
                'equal sides and two equal angles at the base.',
        'topic': 'geometry'},
    {   'grade': '6',
        'subject': 'mathematics',
        'text': 'The perimeter of a shape is the total distance around its outside edge. For a rectangle with length 8 '
                'cm and width 5 cm, the perimeter equals 2 times open bracket 8 plus 5 close bracket equals 2 times 13 '
                'equals 26 cm. For a circle, the perimeter is called the circumference and equals pi times the '
                'diameter.',
        'topic': 'geometry'},
    {   'grade': '6',
        'subject': 'mathematics',
        'text': 'The area of a rectangle is length times width. The area of a triangle is half times base times '
                'height. For example, a triangle with base 10 cm and height 6 cm has an area of half times 10 times 6 '
                'equals 30 square centimetres.',
        'topic': 'geometry'},
    {   'grade': '7',
        'subject': 'mathematics',
        'text': 'Parallel lines are lines that never meet and are always the same distance apart. When a line crosses '
                'two parallel lines, it creates alternate angles that are equal, corresponding angles that are equal, '
                'and co-interior angles that add up to 180 degrees. These properties are used to find unknown angles '
                'in geometric diagrams.',
        'topic': 'geometry'},
    {   'grade': '7',
        'subject': 'mathematics',
        'text': 'Quadrilaterals are four-sided shapes. A parallelogram has two pairs of parallel sides and opposite '
                'angles are equal. A trapezium has exactly one pair of parallel sides, and its area is calculated as '
                'half times the sum of the parallel sides times the height.',
        'topic': 'geometry'},
    {   'grade': '7',
        'subject': 'mathematics',
        'text': 'The area of a circle is pi times r squared, and the circumference is 2 times pi times r, where r is '
                'the radius. For a circle with radius 7 cm, the area is approximately 3.14159 times 49, which is about '
                '153.94 square centimetres. Pi is an irrational number approximately equal to 3.14159.',
        'topic': 'geometry'},
    {   'grade': '8',
        'subject': 'mathematics',
        'text': 'Congruent shapes are identical in size and shape; one can be placed exactly on top of the other. Two '
                'triangles are congruent if they satisfy one of the conditions: SSS (three sides equal), SAS (two '
                'sides and included angle equal), ASA (two angles and included side equal), or RHS (right angle, '
                'hypotenuse, and one side equal). Congruence means all corresponding sides and angles are equal.',
        'topic': 'geometry'},
    {   'grade': '8',
        'subject': 'mathematics',
        'text': 'Similar shapes have the same angles but different sizes; one is an enlargement of the other. The '
                'ratio of corresponding sides is constant and is called the scale factor. If two triangles are similar '
                'and the scale factor is 3, then each side of the larger triangle is 3 times the corresponding side of '
                'the smaller one.',
        'topic': 'geometry'},
    {   'grade': '8',
        'subject': 'mathematics',
        'text': 'The volume of a cuboid is length times width times height. The surface area of a cuboid is 2 times '
                'open bracket length times width plus width times height plus height times length close bracket. For a '
                'cuboid of dimensions 4 cm, 3 cm, and 5 cm, the volume is 60 cubic centimetres and the surface area is '
                '2 times 47 equals 94 square centimetres.',
        'topic': 'geometry'},
    {   'grade': '8',
        'subject': 'mathematics',
        'text': 'Transformations move or change a shape. A translation slides a shape without rotating or reflecting '
                'it, described by a vector. A rotation turns a shape around a centre point through a given angle. A '
                'reflection flips a shape in a mirror line, and an enlargement scales a shape by a given scale factor '
                'from a centre of enlargement.',
        'topic': 'geometry'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'The Pythagorean theorem states that in a right-angled triangle, a squared plus b squared equals c '
                'squared, where c is the hypotenuse. To find the hypotenuse of a triangle with legs 5 cm and 12 cm: c '
                'squared equals 25 plus 144 equals 169, so c equals 13 cm. To find a shorter side, rearrange: a '
                'squared equals c squared minus b squared.',
        'topic': 'geometry'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'Circle theorems describe angle relationships in circles. The angle at the centre of a circle is twice '
                'the angle at the circumference subtended by the same arc. Angles in the same segment are equal. The '
                'angle in a semicircle is always 90 degrees.',
        'topic': 'geometry'},
    {   'grade': '10',
        'subject': 'mathematics',
        'text': 'The volume of a cylinder is pi times r squared times h, and its curved surface area is 2 times pi '
                'times r times h. A cone has volume one third times pi times r squared times h, and a sphere has '
                'volume four thirds times pi times r cubed. These formulas are used in engineering and design to '
                'calculate capacity and material requirements.',
        'topic': 'geometry'},
    {   'grade': '10',
        'subject': 'mathematics',
        'text': 'Coordinate geometry uses algebra to describe geometric shapes. The distance between two points with '
                'coordinates x1, y1 and x2, y2 is the square root of open bracket x2 minus x1 close bracket squared '
                'plus open bracket y2 minus y1 close bracket squared. The midpoint of the line segment joining these '
                'two points is open bracket x1 plus x2 divided by 2, y1 plus y2 divided by 2 close bracket.',
        'topic': 'geometry'},
    {   'grade': '7',
        'subject': 'mathematics',
        'text': 'Probability is a measure of how likely an event is to occur, expressed as a number between 0 and 1. A '
                'probability of 0 means the event is impossible, and a probability of 1 means it is certain. For '
                'example, the probability of rolling a 6 on a fair die is 1 divided by 6, which is approximately '
                '0.167.',
        'topic': 'probability'},
    {   'grade': '7',
        'subject': 'mathematics',
        'text': 'The sample space is the set of all possible outcomes of an experiment. When flipping a coin, the '
                'sample space is heads, tails. When rolling a standard die, the sample space is 1, 2, 3, 4, 5, 6. '
                'Listing the sample space helps calculate the probability of each outcome.',
        'topic': 'probability'},
    {   'grade': '7',
        'subject': 'mathematics',
        'text': 'Theoretical probability is calculated using the formula: probability of an event equals the number of '
                'favourable outcomes divided by the total number of equally likely outcomes. Experimental probability '
                'is found by actually performing an experiment many times and recording the results. As the number of '
                'trials increases, experimental probability gets closer to theoretical probability.',
        'topic': 'probability'},
    {   'grade': '8',
        'subject': 'mathematics',
        'text': 'Two events are mutually exclusive if they cannot both happen at the same time. For example, rolling '
                'an odd number and rolling an even number on a single die are mutually exclusive. The probability that '
                'either of two mutually exclusive events occurs equals the sum of their individual probabilities.',
        'topic': 'probability'},
    {   'grade': '8',
        'subject': 'mathematics',
        'text': 'A Venn diagram uses overlapping circles to show the relationship between sets. The overlap region '
                'represents outcomes that belong to both events. If a bag contains 10 balls, 4 are red, 3 are large, '
                'and 2 are both red and large, then the probability of choosing a ball that is red or large is 4 plus '
                '3 minus 2 divided by 10, which equals 5 over 10 or one half.',
        'topic': 'probability'},
    {   'grade': '8',
        'subject': 'mathematics',
        'text': 'A tree diagram shows all possible outcomes of two or more events by branching at each stage. The '
                'probability at each branch is written on the branch, and the probability of a combined outcome is '
                'found by multiplying along the branches. The probabilities at each set of branches must always add up '
                'to 1.',
        'topic': 'probability'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'Two events are independent if the outcome of one does not affect the outcome of the other. For '
                'independent events, the probability that both occur equals the probability of the first multiplied by '
                'the probability of the second. For example, flipping a coin twice gives a probability of 0.5 times '
                '0.5 equals 0.25 for getting two heads.',
        'topic': 'probability'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'Conditional probability is the probability of an event occurring given that another event has already '
                'occurred. It is written as P of A given B, and calculated as P of A and B divided by P of B. For '
                'example, if a bag has 3 red and 2 blue balls, and you draw one red ball without replacement, the '
                'probability the second ball is red is 2 divided by 4, which is 0.5.',
        'topic': 'probability'},
    {   'grade': '10',
        'subject': 'mathematics',
        'text': 'A permutation is an arrangement of objects where order matters. The number of ways to arrange n '
                'objects in r positions is written as n P r and equals n factorial divided by open bracket n minus r '
                'close bracket factorial. For example, the number of ways to choose and arrange 3 students from a '
                'group of 5 is 5 P 3 equals 60.',
        'topic': 'probability'},
    {   'grade': '10',
        'subject': 'mathematics',
        'text': 'A combination is a selection of objects where order does not matter. The number of ways to choose r '
                'objects from n is written as n C r and equals n factorial divided by open bracket r factorial times '
                'open bracket n minus r close bracket factorial close bracket. For example, choosing 3 flavours from 5 '
                'ice cream flavours gives 5 C 3 equals 10 possible selections.',
        'topic': 'probability'},
    {   'grade': '10',
        'subject': 'mathematics',
        'text': 'Expected value is the average outcome you would expect over many repetitions of an experiment. It is '
                'calculated by multiplying each outcome by its probability and summing the results. For a game where '
                'you win 5 pounds with probability 0.3 and lose 2 pounds with probability 0.7, the expected value is 5 '
                'times 0.3 plus negative 2 times 0.7 equals 1.5 minus 1.4 equals 0.1 pounds.',
        'topic': 'probability'},
    {   'grade': '11',
        'subject': 'mathematics',
        'text': 'The binomial distribution models the number of successes in a fixed number of independent trials, '
                'each with the same probability of success. The probability of exactly r successes in n trials is n C '
                'r times p to the power r times open bracket 1 minus p close bracket to the power open bracket n minus '
                'r close bracket. For example, the probability of exactly 3 heads in 5 fair coin flips is 5 C 3 times '
                '0.5 cubed times 0.5 squared equals 10 times 0.03125 equals 0.3125.',
        'topic': 'probability'},
    {   'grade': '11',
        'subject': 'mathematics',
        'text': 'The complementary event of A is everything that is not A, written as A prime or A complement. The '
                'probability of the complement equals 1 minus the probability of A. This is useful when it is easier '
                'to calculate the probability that an event does not happen; for example, the probability of getting '
                'at least one head in 3 coin flips is 1 minus the probability of getting no heads, which is 1 minus '
                '0.125 equals 0.875.',
        'topic': 'probability'},
    {   'grade': '11',
        'subject': 'mathematics',
        'text': 'A limit describes the value that a function approaches as the input approaches a given value. For '
                'example, as x approaches 2, the function f of x equals x squared approaches 4. Limits are the '
                'foundation of calculus and are used to define both derivatives and integrals.',
        'topic': 'calculus'},
    {   'grade': '11',
        'subject': 'mathematics',
        'text': 'Differentiation finds the rate of change of a function, also called the gradient of the curve at a '
                'point. The derivative of x to the power n is n times x to the power n minus 1. For example, the '
                'derivative of x cubed is 3x squared, and the derivative of 5x squared is 10x.',
        'topic': 'calculus'},
    {   'grade': '11',
        'subject': 'mathematics',
        'text': 'To find the gradient of a curve at a specific point, substitute the x-value into the derivative. For '
                'the function f of x equals x squared plus 3x, the derivative is 2x plus 3. At the point where x '
                'equals 4, the gradient is 2 times 4 plus 3 equals 11. This tells us the slope of the tangent line at '
                'that point.',
        'topic': 'calculus'},
    {   'grade': '11',
        'subject': 'mathematics',
        'text': 'Turning points are where the gradient of a curve equals zero. To find them, set the derivative equal '
                'to zero and solve. For f of x equals x squared minus 4x plus 3, the derivative is 2x minus 4; setting '
                'this to zero gives x equals 2. Substituting back gives f of 2 equals negative 1, so the turning point '
                'is at the coordinates 2, negative 1.',
        'topic': 'calculus'},
    {   'grade': '11',
        'subject': 'mathematics',
        'text': 'The second derivative test determines whether a turning point is a minimum or maximum. If the second '
                'derivative is positive at the turning point, the curve is concave upward and the point is a local '
                'minimum. If the second derivative is negative, the curve is concave downward and the point is a local '
                'maximum.',
        'topic': 'calculus'},
    {   'grade': '12',
        'subject': 'mathematics',
        'text': 'Integration is the reverse process of differentiation and is used to find areas under curves and '
                'accumulate quantities. The integral of x to the power n is x to the power n plus 1 divided by n plus '
                '1, plus a constant C. For example, the integral of 3x squared is x cubed plus C, because '
                'differentiating x cubed gives 3x squared.',
        'topic': 'calculus'},
    {   'grade': '12',
        'subject': 'mathematics',
        'text': 'A definite integral calculates the exact area between a curve and the x-axis between two limits. The '
                'definite integral of f of x from a to b is written with a at the bottom and b at the top of the '
                'integral sign, and equals the antiderivative evaluated at b minus the antiderivative evaluated at a. '
                'For the integral of x squared from 1 to 3, we get 27 divided by 3 minus 1 divided by 3 equals 9 minus '
                'one third equals 26 thirds.',
        'topic': 'calculus'},
    {   'grade': '12',
        'subject': 'mathematics',
        'text': 'The chain rule is used to differentiate composite functions, where one function is inside another. If '
                'y equals f of g of x, then the derivative is f prime of g of x times g prime of x. For example, to '
                'differentiate y equals open bracket 3x plus 2 close bracket to the power 5, let u equal 3x plus 2, so '
                'y equals u to the power 5; the derivative is 5u to the power 4 times 3 equals 15 times open bracket '
                '3x plus 2 close bracket to the power 4.',
        'topic': 'calculus'},
    {   'grade': '12',
        'subject': 'mathematics',
        'text': 'The product rule is used to differentiate the product of two functions. If y equals u times v, then '
                'the derivative is u times the derivative of v plus v times the derivative of u. For example, to '
                'differentiate y equals x squared times e to the power x, let u equal x squared and v equal e to the '
                'power x; the derivative is x squared times e to the power x plus 2x times e to the power x, which '
                'simplifies to e to the power x times open bracket x squared plus 2x close bracket.',
        'topic': 'calculus'},
    {   'grade': '12',
        'subject': 'mathematics',
        'text': 'Optimisation problems use calculus to find the maximum or minimum value of a quantity. For example, '
                'to find the dimensions of a rectangle with perimeter 20 cm that has maximum area: let one side be x, '
                'so the other is 10 minus x and the area is A equals x times open bracket 10 minus x close bracket '
                'equals 10x minus x squared. Differentiating gives 10 minus 2x; setting to zero gives x equals 5, '
                'meaning the rectangle is a square with area 25 square centimetres.',
        'topic': 'calculus'},
    {   'grade': '12',
        'subject': 'mathematics',
        'text': "Rates of change are a direct application of differentiation. If a car's position in metres is given "
                'by s equals t cubed minus 3t squared plus 4t, then the velocity is the derivative ds by dt equals 3t '
                'squared minus 6t plus 4, and the acceleration is the second derivative, 6t minus 6. At t equals 2 '
                'seconds, the velocity is 12 minus 12 plus 4 equals 4 metres per second.',
        'topic': 'calculus'},
    {   'grade': '12',
        'subject': 'mathematics',
        'text': 'Integration by substitution simplifies integrals by replacing a complex expression with a single '
                'variable. For example, to find the integral of 2x times open bracket x squared plus 1 close bracket '
                'to the power 4, let u equal x squared plus 1, so du by dx equals 2x. The integral becomes the '
                'integral of u to the power 4 du, which equals u to the power 5 divided by 5 plus C, giving open '
                'bracket x squared plus 1 close bracket to the power 5 divided by 5 plus C.',
        'topic': 'calculus'},
    {   'grade': '6',
        'subject': 'mathematics',
        'text': 'A prime number is a whole number greater than 1 that has exactly two factors: 1 and itself. The first '
                'ten prime numbers are 2, 3, 5, 7, 11, 13, 17, 19, 23, and 29. The number 2 is the only even prime '
                'number; all other even numbers have 2 as a factor and are therefore not prime.',
        'topic': 'number theory'},
    {   'grade': '6',
        'subject': 'mathematics',
        'text': 'Factors of a number are the whole numbers that divide into it exactly with no remainder. The factors '
                'of 12 are 1, 2, 3, 4, 6, and 12. Every number has at least two factors, 1 and itself; prime numbers '
                'have exactly two factors.',
        'topic': 'number theory'},
    {   'grade': '6',
        'subject': 'mathematics',
        'text': 'Multiples of a number are found by multiplying it by 1, 2, 3, and so on. The multiples of 4 are 4, 8, '
                '12, 16, 20, and so on. Recognising multiples is useful for finding the lowest common multiple of two '
                'numbers.',
        'topic': 'number theory'},
    {   'grade': '7',
        'subject': 'mathematics',
        'text': 'The Highest Common Factor, or HCF, of two numbers is the largest number that divides both exactly. To '
                'find the HCF of 24 and 36, list their factors: factors of 24 are 1, 2, 3, 4, 6, 8, 12, 24 and factors '
                'of 36 are 1, 2, 3, 4, 6, 9, 12, 18, 36. The largest factor in both lists is 12, so HCF equals 12.',
        'topic': 'number theory'},
    {   'grade': '7',
        'subject': 'mathematics',
        'text': 'The Lowest Common Multiple, or LCM, of two numbers is the smallest number that is a multiple of both. '
                'To find the LCM of 4 and 6, list multiples: multiples of 4 are 4, 8, 12, 16 and multiples of 6 are 6, '
                '12, 18. The smallest number in both lists is 12, so LCM equals 12. LCM is used when adding or '
                'subtracting fractions with different denominators.',
        'topic': 'number theory'},
    {   'grade': '7',
        'subject': 'mathematics',
        'text': 'Every whole number greater than 1 can be written as a product of prime numbers in exactly one way; '
                'this is called the prime factorisation. For example, 60 equals 2 times 2 times 3 times 5, written as '
                '2 squared times 3 times 5. Prime factorisation can be found using a factor tree by repeatedly '
                'splitting each composite number into two factors.',
        'topic': 'number theory'},
    {   'grade': '7',
        'subject': 'mathematics',
        'text': 'Indices, also called powers or exponents, show repeated multiplication. The expression 2 to the power '
                '5 means 2 times 2 times 2 times 2 times 2, which equals 32. The rules of indices include: a to the '
                'power m times a to the power n equals a to the power m plus n, and a to the power m divided by a to '
                'the power n equals a to the power m minus n.',
        'topic': 'number theory'},
    {   'grade': '8',
        'subject': 'mathematics',
        'text': 'Standard form, also called scientific notation, is a way to write very large or very small numbers. A '
                'number in standard form is written as a number between 1 and 10 multiplied by a power of 10. For '
                'example, 3,700,000 is written as 3.7 times 10 to the power 6, and 0.000045 is written as 4.5 times 10 '
                'to the power negative 5.',
        'topic': 'number theory'},
    {   'grade': '8',
        'subject': 'mathematics',
        'text': 'Rational numbers are numbers that can be written as a fraction of two integers, where the denominator '
                'is not zero. Examples include 3, negative 5, one half, and 0.75. Irrational numbers cannot be '
                'expressed as fractions; their decimal expansions are non-terminating and non-repeating. Well-known '
                'examples include pi and the square root of 2.',
        'topic': 'number theory'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'Surds are irrational numbers written using the square root symbol that cannot be simplified to a '
                'whole number or fraction. For example, the square root of 3 and the square root of 5 are surds. Surds '
                'can be simplified when the number under the root has a perfect square factor; for instance, the '
                'square root of 12 equals the square root of 4 times 3, which equals 2 times the square root of 3.',
        'topic': 'number theory'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'Rationalising the denominator means rewriting a fraction so that there is no surd in the denominator. '
                'To rationalise 1 divided by the square root of 5, multiply both numerator and denominator by the '
                'square root of 5 to get the square root of 5 divided by 5. For expressions like 1 divided by open '
                'bracket 2 plus the square root of 3 close bracket, multiply by the conjugate 2 minus the square root '
                'of 3 to eliminate the surd.',
        'topic': 'number theory'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'A number pattern or sequence follows a specific rule. A geometric sequence has a constant ratio '
                'between consecutive terms. For example, 2, 6, 18, 54 is a geometric sequence with a common ratio of '
                '3. The nth term of a geometric sequence is a times r to the power n minus 1, where a is the first '
                'term and r is the common ratio.',
        'topic': 'number theory'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'Negative and fractional indices extend the laws of indices. Any number to the power zero equals 1; '
                'for example, 7 to the power 0 equals 1. A negative index means the reciprocal: 2 to the power '
                'negative 3 equals 1 divided by 2 cubed equals 1 over 8. A fractional index denotes a root: 8 to the '
                'power one third equals the cube root of 8 equals 2.',
        'topic': 'number theory'},
    {   'grade': '10',
        'subject': 'mathematics',
        'text': 'The tangent function is undefined at 90 degrees and 270 degrees because cosine equals zero at those '
                'angles, making the ratio sine over cosine involve division by zero. The graph of tangent repeats '
                'every 180 degrees and has vertical asymptotes at these undefined points. Between consecutive '
                'asymptotes, the tangent curve rises steeply from negative infinity to positive infinity.',
        'topic': 'trigonometry'},
    {   'grade': '10',
        'subject': 'mathematics',
        'text': 'The exact values of sine, cosine, and tangent for common angles should be memorised. Sine of 30 '
                'degrees equals one half, sine of 45 degrees equals root 2 over 2, and sine of 60 degrees equals root '
                '3 over 2. Cosine of 30 degrees equals root 3 over 2, cosine of 45 degrees equals root 2 over 2, and '
                'cosine of 60 degrees equals one half.',
        'topic': 'trigonometry'},
    {   'grade': '11',
        'subject': 'mathematics',
        'text': 'The compound angle formula for sine states that sine of open bracket A plus B close bracket equals '
                'sine A cosine B plus cosine A sine B. For example, sine of 75 degrees equals sine of open bracket 45 '
                'plus 30 close bracket equals sine 45 cosine 30 plus cosine 45 sine 30, which equals root 2 over 2 '
                'times root 3 over 2 plus root 2 over 2 times one half, giving root 6 plus root 2 all over 4.',
        'topic': 'trigonometry'},
    {   'grade': '11',
        'subject': 'mathematics',
        'text': 'The amplitude of a trigonometric graph is the distance from the midline to the maximum or minimum '
                'value. For y equals 3 sine x, the amplitude is 3, so the graph oscillates between negative 3 and '
                'positive 3. The period of a trig function is the length of one complete cycle; for y equals sine of '
                '2x, the period is 360 divided by 2 equals 180 degrees.',
        'topic': 'trigonometry'},
    {   'grade': '12',
        'subject': 'mathematics',
        'text': 'Trigonometric form of a complex number expresses it as r times open bracket cosine theta plus i sine '
                'theta close bracket, where r is the modulus and theta is the argument. Multiplying two complex '
                'numbers in trig form means multiplying their moduli and adding their arguments. This leads naturally '
                "to De Moivre's theorem, which states that r to the power n times open bracket cosine n theta plus i "
                'sine n theta close bracket equals r times open bracket cosine theta plus i sine theta close bracket '
                'raised to the power n.',
        'topic': 'trigonometry'},
    {   'grade': '11',
        'subject': 'mathematics',
        'text': 'The area of any triangle can be found using trigonometry with the formula: area equals one half times '
                'a times b times sine C, where a and b are two sides and C is the angle between them. For a triangle '
                'with sides 8 cm and 5 cm and an included angle of 40 degrees, the area equals one half times 8 times '
                '5 times sine 40, which is approximately 12.86 square centimetres.',
        'topic': 'trigonometry'},
    {   'grade': '12',
        'subject': 'mathematics',
        'text': 'Solving trigonometric equations in a given interval requires finding all valid solutions, not just '
                'the principal value. For cosine theta equals negative 0.5 in the interval 0 to 360 degrees, the '
                'principal value is 120 degrees. Because cosine is also negative in the third quadrant, the second '
                'solution is 360 minus 120 equals 240 degrees, giving solutions of 120 degrees and 240 degrees.',
        'topic': 'trigonometry'},
    {   'grade': '7',
        'subject': 'mathematics',
        'text': 'Like terms are terms that contain the same variable raised to the same power. For example, 3x squared '
                'and 7x squared are like terms and can be combined to give 10x squared. However, 3x squared and 3x are '
                'not like terms because the powers of x differ, so they cannot be combined.',
        'topic': 'algebra'},
    {   'grade': '8',
        'subject': 'mathematics',
        'text': 'The difference of two squares identity states that a squared minus b squared equals open bracket a '
                'plus b close bracket times open bracket a minus b close bracket. For example, x squared minus 25 '
                'factorises to open bracket x plus 5 close bracket times open bracket x minus 5 close bracket. This '
                'pattern is useful for quickly factorising expressions without trial and error.',
        'topic': 'algebra'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'A function is a rule that maps each input value to exactly one output value. The function f of x '
                'equals 2x plus 1 maps x equals 3 to f of 3 equals 7. The domain is the set of all allowed input '
                'values, and the range is the set of all possible output values.',
        'topic': 'algebra'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'Indices in algebra follow the same rules as numerical indices. The expression x to the power 3 times '
                'x to the power 4 equals x to the power 7, because the indices are added. The expression x to the '
                'power 6 divided by x to the power 2 equals x to the power 4, because the indices are subtracted. Open '
                'bracket x to the power 3 close bracket squared equals x to the power 6, because the indices are '
                'multiplied.',
        'topic': 'algebra'},
    {   'grade': '8',
        'subject': 'mathematics',
        'text': 'Solving a pair of simultaneous equations graphically means finding the point of intersection of two '
                'straight lines. The x and y coordinates of that point are the solutions to both equations. For '
                'example, y equals 2x plus 1 and y equals negative x plus 7 intersect at x equals 2, y equals 5, which '
                'can be verified by substituting into both equations.',
        'topic': 'algebra'},
    {   'grade': '10',
        'subject': 'mathematics',
        'text': 'Polynomial long division is used to divide one polynomial by another. To divide x cubed plus 2x '
                'squared minus 5x minus 6 by x minus 2, find how many times x divides into x cubed, which gives x '
                'squared. Multiply, subtract, and repeat the process until no remainder remains. The result here is x '
                'squared plus 4x plus 3, which factorises further to open bracket x plus 1 close bracket times open '
                'bracket x plus 3 close bracket.',
        'topic': 'algebra'},
    {   'grade': '10',
        'subject': 'mathematics',
        'text': 'The discriminant b squared minus 4ac determines the nature of the roots of a quadratic. If the '
                'discriminant is greater than zero, the quadratic has two distinct real roots. If it equals zero, '
                'there is exactly one repeated root. If it is less than zero, there are no real roots, only complex '
                'roots. For example, for 2x squared minus 4x plus 5, the discriminant is 16 minus 40 equals negative '
                '24, so there are no real roots.',
        'topic': 'algebra'},
    {   'grade': '8',
        'subject': 'mathematics',
        'text': 'Pictograms and bar charts are simple ways to display categorical data. In a bar chart, the height of '
                'each bar represents the frequency of each category, and the bars are separated by gaps to show that '
                'the data is discrete. The vertical axis should start at zero to avoid misleading visual impressions.',
        'topic': 'statistics'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'Outliers are data values that lie far from the rest of the data set. In a box plot, a value is '
                'typically considered an outlier if it falls more than 1.5 times the interquartile range above the '
                'upper quartile or below the lower quartile. Outliers can distort the mean significantly but have '
                'little effect on the median.',
        'topic': 'statistics'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'When estimating the mean from a grouped frequency table, use the midpoint of each class interval to '
                'represent all values in that class. Multiply each midpoint by its frequency, sum all these products, '
                'then divide by the total frequency. This gives an estimate, not the exact mean, because we do not '
                'know the individual values within each class.',
        'topic': 'statistics'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'Two-way tables display data that is categorised by two different variables. Reading across rows and '
                'down columns allows you to find joint frequencies, marginal frequencies, and conditional '
                'probabilities. For example, a two-way table might show whether students passed a test, broken down by '
                'gender, allowing comparison of pass rates between groups.',
        'topic': 'statistics'},
    {   'grade': '10',
        'subject': 'mathematics',
        'text': 'The interquartile range is a better measure of spread than the range when data contains outliers '
                'because it focuses on the middle 50 percent of the data. The lower quartile is the median of the '
                'lower half of the data and the upper quartile is the median of the upper half. A small interquartile '
                'range means the central data is tightly clustered.',
        'topic': 'statistics'},
    {   'grade': '11',
        'subject': 'mathematics',
        'text': 'Hypothesis testing uses sample data to make decisions about a population. A null hypothesis states '
                'that there is no effect or no difference, while an alternative hypothesis states that there is. The '
                'p-value is the probability of getting a result at least as extreme as the observed one if the null '
                'hypothesis were true; a small p-value, typically less than 0.05, provides evidence to reject the null '
                'hypothesis.',
        'topic': 'statistics'},
    {   'grade': '11',
        'subject': 'mathematics',
        'text': 'Regression analysis finds the equation of the line of best fit for bivariate data. The least squares '
                'regression line minimises the sum of the squared vertical distances from each data point to the line. '
                'The equation takes the form y equals a plus bx, where b is the gradient and a is the y-intercept, and '
                'is used to predict the value of y for a given x.',
        'topic': 'statistics'},
    {   'grade': '11',
        'subject': 'mathematics',
        'text': 'The standard normal distribution has a mean of 0 and a standard deviation of 1. Any normal '
                'distribution can be converted to the standard normal by computing a z-score, which equals the value '
                'minus the mean, divided by the standard deviation. Z-scores allow us to find probabilities by looking '
                'up areas under the standard normal curve in a table.',
        'topic': 'statistics'},
    {   'grade': '7',
        'subject': 'mathematics',
        'text': 'Interior angles of a polygon sum to 180 times open bracket n minus 2 close bracket degrees, where n '
                'is the number of sides. For a hexagon with 6 sides, the sum of interior angles is 180 times 4 equals '
                '720 degrees. Each interior angle of a regular hexagon is 720 divided by 6 equals 120 degrees.',
        'topic': 'geometry'},
    {   'grade': '7',
        'subject': 'mathematics',
        'text': 'The exterior angle of a triangle equals the sum of the two non-adjacent interior angles. For example, '
                'if two interior angles of a triangle are 45 degrees and 70 degrees, the exterior angle at the third '
                'vertex is 45 plus 70 equals 115 degrees. The sum of all exterior angles of any convex polygon is '
                'always 360 degrees.',
        'topic': 'geometry'},
    {   'grade': '10',
        'subject': 'mathematics',
        'text': 'Vectors describe a movement in terms of direction and distance. A vector from point A to point B is '
                'written with an arrow above AB or in column form with horizontal and vertical components. Adding '
                'vectors means combining their components: open bracket 3, 2 close bracket plus open bracket 1, '
                'negative 4 close bracket equals open bracket 4, negative 2 close bracket.',
        'topic': 'geometry'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'A tangent to a circle is a straight line that touches the circle at exactly one point, called the '
                'point of tangency. The angle between a tangent and the radius drawn to the point of tangency is '
                'always 90 degrees. Two tangents drawn from an external point to a circle are equal in length.',
        'topic': 'geometry'},
    {   'grade': '10',
        'subject': 'mathematics',
        'text': 'When shapes are enlarged with a scale factor k, areas scale by a factor of k squared and volumes '
                'scale by a factor of k cubed. If two similar solids have a length ratio of 1 to 3, their surface '
                'areas are in the ratio 1 to 9 and their volumes are in the ratio 1 to 27. This is crucial in '
                'engineering and modelling when scaling between prototypes and real objects.',
        'topic': 'geometry'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'A locus is the set of all points that satisfy a given condition. The locus of points equidistant from '
                'a fixed point is a circle. The locus of points equidistant from two fixed points is the perpendicular '
                'bisector of the line segment joining those two points. Loci problems often require combining two or '
                'more conditions.',
        'topic': 'geometry'},
    {   'grade': '8',
        'subject': 'mathematics',
        'text': 'The gradient of a straight line on a coordinate grid is rise divided by run, which equals the change '
                'in y divided by the change in x. For two points with coordinates 1, 3 and 4, 9, the gradient is 9 '
                'minus 3 divided by 4 minus 1 equals 6 over 3 equals 2. The equation of the line through these points '
                'is y equals 2x plus 1.',
        'topic': 'geometry'},
    {   'grade': '8',
        'subject': 'mathematics',
        'text': 'Bearings are angles measured clockwise from North, always written as three figures. A bearing of 045 '
                'degrees means 45 degrees clockwise from North, which is northeast. Bearings are used in navigation '
                'and trigonometry problems involving distances and directions.',
        'topic': 'geometry'},
    {   'grade': '7',
        'subject': 'mathematics',
        'text': 'Relative frequency is used to estimate probability from experimental data. If a drawing pin lands '
                'point up 63 times out of 100 throws, the relative frequency is 0.63. As the number of trials '
                'increases, the relative frequency becomes a more reliable estimate of the true theoretical '
                'probability.',
        'topic': 'probability'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'The addition rule for probability states that P of A or B equals P of A plus P of B minus P of A and '
                'B. The subtraction of P of A and B avoids double-counting the outcomes in the overlap. If two events '
                'are mutually exclusive, P of A and B equals 0, so the rule simplifies to P of A plus P of B.',
        'topic': 'probability'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'When drawing items without replacement, the total number of outcomes decreases with each draw, making '
                'successive events dependent. For example, if a bag contains 5 red and 3 blue counters, the '
                'probability of drawing red then blue is 5 over 8 times 3 over 7 equals 15 over 56. Tree diagrams '
                'clearly display how probabilities change after each draw.',
        'topic': 'probability'},
    {   'grade': '10',
        'subject': 'mathematics',
        'text': 'The multiplication rule for independent events states that P of A and B equals P of A times P of B. '
                'Two events are independent when knowing the outcome of one gives no information about the other. A '
                'simple check: if P of A given B equals P of A, the events are independent.',
        'topic': 'probability'},
    {   'grade': '11',
        'subject': 'mathematics',
        'text': "Bayes' theorem allows us to update the probability of an event based on new evidence. It states that "
                'P of A given B equals P of B given A times P of A, divided by P of B. For example, if a medical test '
                'is 95 percent accurate and 1 percent of the population has a disease, a positive test result does not '
                "mean the patient definitely has the disease; Bayes' theorem shows the actual probability may still be "
                'relatively low.',
        'topic': 'probability'},
    {   'grade': '11',
        'subject': 'mathematics',
        'text': 'The geometric distribution models the number of trials needed to achieve the first success in a '
                'sequence of independent Bernoulli trials. The probability of the first success occurring on the nth '
                'trial is open bracket 1 minus p close bracket to the power n minus 1 times p, where p is the '
                'probability of success. The expected number of trials until the first success is 1 divided by p.',
        'topic': 'probability'},
    {   'grade': '11',
        'subject': 'mathematics',
        'text': 'The Poisson distribution models the number of events occurring in a fixed interval of time or space '
                'when events happen independently at a constant average rate. If the average number of events is '
                'lambda, the probability of exactly k events is e to the power negative lambda times lambda to the '
                'power k, divided by k factorial. It is commonly used to model arrivals, such as customers entering a '
                'shop or calls received per hour.',
        'topic': 'probability'},
    {   'grade': '12',
        'subject': 'mathematics',
        'text': 'The quotient rule is used to differentiate a function that is one expression divided by another. If y '
                'equals u divided by v, then the derivative equals v times the derivative of u minus u times the '
                'derivative of v, all divided by v squared. For example, to differentiate y equals x squared divided '
                'by open bracket x plus 1 close bracket, the derivative is open bracket open bracket x plus 1 close '
                'bracket times 2x minus x squared times 1 close bracket divided by open bracket x plus 1 close bracket '
                'squared, which simplifies to x squared plus 2x divided by open bracket x plus 1 close bracket '
                'squared.',
        'topic': 'calculus'},
    {   'grade': '12',
        'subject': 'mathematics',
        'text': 'The derivative of the natural exponential function e to the power x is itself, e to the power x. The '
                'derivative of the natural logarithm ln of x is 1 divided by x, for x greater than 0. These results, '
                'combined with the chain rule, allow differentiation of expressions like e to the power 3x squared, '
                'whose derivative is 6x times e to the power 3x squared.',
        'topic': 'calculus'},
    {   'grade': '12',
        'subject': 'mathematics',
        'text': 'The trapezium rule is a numerical method for estimating the area under a curve. The area is '
                'approximated by dividing it into trapezoids of equal width h and summing their areas using the '
                'formula: half times h times open bracket y zero plus 2 times open bracket y one plus y two plus dot '
                'dot dot plus y n minus 1 close bracket plus y n close bracket. The more strips used, the closer the '
                'estimate is to the true integral.',
        'topic': 'calculus'},
    {   'grade': '12',
        'subject': 'mathematics',
        'text': 'Integration can be used to find the area between two curves. If f of x is above g of x in the '
                'interval from a to b, the area between them is the integral from a to b of open bracket f of x minus '
                'g of x close bracket dx. First find the x values where the curves intersect by solving f of x equals '
                'g of x, as these form the limits of integration.',
        'topic': 'calculus'},
    {   'grade': '12',
        'subject': 'mathematics',
        'text': 'Implicit differentiation is used when y cannot be easily expressed as a function of x alone. '
                'Differentiate both sides of the equation with respect to x, applying the chain rule to any terms '
                'involving y by multiplying by dy by dx. For the circle equation x squared plus y squared equals 25, '
                'differentiating gives 2x plus 2y times dy by dx equals 0, so dy by dx equals negative x divided by y.',
        'topic': 'calculus'},
    {   'grade': '12',
        'subject': 'mathematics',
        'text': 'Kinematics uses calculus to connect displacement, velocity, and acceleration. Velocity is the '
                'derivative of displacement with respect to time, and acceleration is the derivative of velocity with '
                'respect to time. Conversely, displacement is the integral of velocity and velocity is the integral of '
                "acceleration. If a particle's velocity is v equals 4t minus t squared metres per second, its "
                'displacement after 3 seconds is the integral from 0 to 3 of open bracket 4t minus t squared close '
                'bracket dt, which equals 18 minus 9 equals 9 metres.',
        'topic': 'calculus'},
    {   'grade': '6',
        'subject': 'mathematics',
        'text': 'The Sieve of Eratosthenes is an ancient method for finding all prime numbers up to a given limit. '
                'Start by writing all numbers from 2 upward, then cross out all multiples of 2 greater than 2, then '
                'all multiples of 3 greater than 3, and so on. The numbers that remain are prime. For example, '
                'applying the sieve up to 30 reveals the primes 2, 3, 5, 7, 11, 13, 17, 19, 23, and 29.',
        'topic': 'number theory'},
    {   'grade': '6',
        'subject': 'mathematics',
        'text': 'Divisibility rules are shortcuts to check whether a number is divisible by small integers without '
                'performing full division. A number is divisible by 2 if its last digit is even, by 3 if its digit sum '
                'is divisible by 3, by 5 if it ends in 0 or 5, and by 9 if its digit sum is divisible by 9. For '
                'example, 324 has a digit sum of 9, so it is divisible by both 3 and 9.',
        'topic': 'number theory'},
    {   'grade': '7',
        'subject': 'mathematics',
        'text': 'The HCF and LCM of two numbers can be found efficiently using their prime factorisations. The HCF is '
                'the product of the prime factors common to both numbers, each taken to the lowest power. The LCM is '
                'the product of all prime factors from either number, each taken to the highest power. For 12 equals 2 '
                'squared times 3 and 18 equals 2 times 3 squared, the HCF is 2 times 3 equals 6 and the LCM is 2 '
                'squared times 3 squared equals 36.',
        'topic': 'number theory'},
    {   'grade': '8',
        'subject': 'mathematics',
        'text': 'Recurring decimals are rational numbers whose decimal expansion repeats indefinitely. The fraction '
                'one third equals 0.333 recurring, and one seventh equals 0.142857 recurring. To convert a recurring '
                'decimal to a fraction, let x equal the decimal, multiply by a suitable power of 10 to shift the '
                'recurring block, subtract the original equation, and solve for x.',
        'topic': 'number theory'},
    {   'grade': '8',
        'subject': 'mathematics',
        'text': 'The index law for a power of zero states that any non-zero number raised to the power 0 equals 1. '
                'This follows from the subtraction rule: a to the power n divided by a to the power n equals a to the '
                'power n minus n equals a to the power 0, and any number divided by itself equals 1. Zero to the power '
                'zero is considered indeterminate in most mathematical contexts.',
        'topic': 'number theory'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': "Euclid's algorithm is an efficient method for finding the HCF of two numbers by repeated division. "
                'Divide the larger number by the smaller, note the remainder, then replace the larger number with the '
                'smaller and the smaller with the remainder, repeating until the remainder is zero. For HCF of 252 and '
                '105: 252 equals 2 times 105 plus 42; 105 equals 2 times 42 plus 21; 42 equals 2 times 21 plus 0; so '
                'HCF equals 21.',
        'topic': 'number theory'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'Modular arithmetic deals with remainders after division. We say a is congruent to b modulo n if a and '
                'b have the same remainder when divided by n. For example, 17 is congruent to 2 modulo 5 because both '
                'leave a remainder of 2 when divided by 5. Modular arithmetic is used in cryptography, calendar '
                'calculations, and computer science.',
        'topic': 'number theory'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'An arithmetic series is the sum of the terms of an arithmetic sequence. The sum of the first n terms '
                'is S equals n divided by 2 times open bracket first term plus last term close bracket, or '
                'equivalently S equals n divided by 2 times open bracket 2a plus open bracket n minus 1 close bracket '
                'times d close bracket. For the series 1 plus 3 plus 5 plus dot dot dot plus 99, n equals 50, a equals '
                '1, and l equals 99, giving S equals 50 divided by 2 times 100 equals 2500.',
        'topic': 'number theory'},
    {   'grade': '10',
        'subject': 'mathematics',
        'text': 'The tangent function is undefined at 90 degrees and 270 degrees because cosine equals zero at those '
                'angles, making the ratio sine over cosine involve division by zero. The graph of tangent repeats '
                'every 180 degrees and has vertical asymptotes at these undefined points. Between consecutive '
                'asymptotes, the tangent curve rises steeply from negative infinity to positive infinity.',
        'topic': 'trigonometry'},
    {   'grade': '10',
        'subject': 'mathematics',
        'text': 'The exact values of sine, cosine, and tangent for common angles should be memorised. Sine of 30 '
                'degrees equals one half, sine of 45 degrees equals root 2 over 2, and sine of 60 degrees equals root '
                '3 over 2. Cosine of 30 degrees equals root 3 over 2, cosine of 45 degrees equals root 2 over 2, and '
                'cosine of 60 degrees equals one half.',
        'topic': 'trigonometry'},
    {   'grade': '11',
        'subject': 'mathematics',
        'text': 'The compound angle formula for sine states that sine of open bracket A plus B close bracket equals '
                'sine A cosine B plus cosine A sine B. For example, sine of 75 degrees equals sine of open bracket 45 '
                'plus 30 close bracket equals sine 45 cosine 30 plus cosine 45 sine 30, which equals root 2 over 2 '
                'times root 3 over 2 plus root 2 over 2 times one half, giving root 6 plus root 2 all over 4.',
        'topic': 'trigonometry'},
    {   'grade': '11',
        'subject': 'mathematics',
        'text': 'The amplitude of a trigonometric graph is the distance from the midline to the maximum or minimum '
                'value. For y equals 3 sine x, the amplitude is 3, so the graph oscillates between negative 3 and '
                'positive 3. The period of a trig function is the length of one complete cycle; for y equals sine of '
                '2x, the period is 360 divided by 2 equals 180 degrees.',
        'topic': 'trigonometry'},
    {   'grade': '12',
        'subject': 'mathematics',
        'text': 'Trigonometric form of a complex number expresses it as r times open bracket cosine theta plus i sine '
                'theta close bracket, where r is the modulus and theta is the argument. Multiplying two complex '
                'numbers in trig form means multiplying their moduli and adding their arguments. This leads naturally '
                "to De Moivre's theorem, which states that r to the power n times open bracket cosine n theta plus i "
                'sine n theta close bracket equals r times open bracket cosine theta plus i sine theta close bracket '
                'raised to the power n.',
        'topic': 'trigonometry'},
    {   'grade': '11',
        'subject': 'mathematics',
        'text': 'The area of any triangle can be found using trigonometry with the formula: area equals one half times '
                'a times b times sine C, where a and b are two sides and C is the angle between them. For a triangle '
                'with sides 8 cm and 5 cm and an included angle of 40 degrees, the area equals one half times 8 times '
                '5 times sine 40, which is approximately 12.86 square centimetres.',
        'topic': 'trigonometry'},
    {   'grade': '12',
        'subject': 'mathematics',
        'text': 'Solving trigonometric equations in a given interval requires finding all valid solutions, not just '
                'the principal value. For cosine theta equals negative 0.5 in the interval 0 to 360 degrees, the '
                'principal value is 120 degrees. Because cosine is also negative in the third quadrant, the second '
                'solution is 360 minus 120 equals 240 degrees, giving solutions of 120 degrees and 240 degrees.',
        'topic': 'trigonometry'},
    {   'grade': '7',
        'subject': 'mathematics',
        'text': 'Like terms are terms that contain the same variable raised to the same power. For example, 3x squared '
                'and 7x squared are like terms and can be combined to give 10x squared. However, 3x squared and 3x are '
                'not like terms because the powers of x differ, so they cannot be combined.',
        'topic': 'algebra'},
    {   'grade': '8',
        'subject': 'mathematics',
        'text': 'The difference of two squares identity states that a squared minus b squared equals open bracket a '
                'plus b close bracket times open bracket a minus b close bracket. For example, x squared minus 25 '
                'factorises to open bracket x plus 5 close bracket times open bracket x minus 5 close bracket. This '
                'pattern is useful for quickly factorising expressions without trial and error.',
        'topic': 'algebra'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'A function is a rule that maps each input value to exactly one output value. The function f of x '
                'equals 2x plus 1 maps x equals 3 to f of 3 equals 7. The domain is the set of all allowed input '
                'values, and the range is the set of all possible output values.',
        'topic': 'algebra'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'Indices in algebra follow the same rules as numerical indices. The expression x to the power 3 times '
                'x to the power 4 equals x to the power 7, because the indices are added. The expression x to the '
                'power 6 divided by x to the power 2 equals x to the power 4, because the indices are subtracted. Open '
                'bracket x to the power 3 close bracket squared equals x to the power 6, because the indices are '
                'multiplied.',
        'topic': 'algebra'},
    {   'grade': '8',
        'subject': 'mathematics',
        'text': 'Solving a pair of simultaneous equations graphically means finding the point of intersection of two '
                'straight lines. The x and y coordinates of that point are the solutions to both equations. For '
                'example, y equals 2x plus 1 and y equals negative x plus 7 intersect at x equals 2, y equals 5, which '
                'can be verified by substituting into both equations.',
        'topic': 'algebra'},
    {   'grade': '10',
        'subject': 'mathematics',
        'text': 'Polynomial long division is used to divide one polynomial by another. To divide x cubed plus 2x '
                'squared minus 5x minus 6 by x minus 2, find how many times x divides into x cubed, which gives x '
                'squared. Multiply, subtract, and repeat the process until no remainder remains. The result here is x '
                'squared plus 4x plus 3, which factorises further to open bracket x plus 1 close bracket times open '
                'bracket x plus 3 close bracket.',
        'topic': 'algebra'},
    {   'grade': '10',
        'subject': 'mathematics',
        'text': 'The discriminant b squared minus 4ac determines the nature of the roots of a quadratic. If the '
                'discriminant is greater than zero, the quadratic has two distinct real roots. If it equals zero, '
                'there is exactly one repeated root. If it is less than zero, there are no real roots, only complex '
                'roots. For example, for 2x squared minus 4x plus 5, the discriminant is 16 minus 40 equals negative '
                '24, so there are no real roots.',
        'topic': 'algebra'},
    {   'grade': '8',
        'subject': 'mathematics',
        'text': 'Pictograms and bar charts are simple ways to display categorical data. In a bar chart, the height of '
                'each bar represents the frequency of each category, and the bars are separated by gaps to show that '
                'the data is discrete. The vertical axis should start at zero to avoid misleading visual impressions.',
        'topic': 'statistics'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'Outliers are data values that lie far from the rest of the data set. In a box plot, a value is '
                'typically considered an outlier if it falls more than 1.5 times the interquartile range above the '
                'upper quartile or below the lower quartile. Outliers can distort the mean significantly but have '
                'little effect on the median.',
        'topic': 'statistics'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'When estimating the mean from a grouped frequency table, use the midpoint of each class interval to '
                'represent all values in that class. Multiply each midpoint by its frequency, sum all these products, '
                'then divide by the total frequency. This gives an estimate, not the exact mean, because we do not '
                'know the individual values within each class.',
        'topic': 'statistics'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'Two-way tables display data that is categorised by two different variables. Reading across rows and '
                'down columns allows you to find joint frequencies, marginal frequencies, and conditional '
                'probabilities. For example, a two-way table might show whether students passed a test, broken down by '
                'gender, allowing comparison of pass rates between groups.',
        'topic': 'statistics'},
    {   'grade': '10',
        'subject': 'mathematics',
        'text': 'The interquartile range is a better measure of spread than the range when data contains outliers '
                'because it focuses on the middle 50 percent of the data. The lower quartile is the median of the '
                'lower half of the data and the upper quartile is the median of the upper half. A small interquartile '
                'range means the central data is tightly clustered.',
        'topic': 'statistics'},
    {   'grade': '11',
        'subject': 'mathematics',
        'text': 'Hypothesis testing uses sample data to make decisions about a population. A null hypothesis states '
                'that there is no effect or no difference, while an alternative hypothesis states that there is. The '
                'p-value is the probability of getting a result at least as extreme as the observed one if the null '
                'hypothesis were true; a small p-value, typically less than 0.05, provides evidence to reject the null '
                'hypothesis.',
        'topic': 'statistics'},
    {   'grade': '11',
        'subject': 'mathematics',
        'text': 'Regression analysis finds the equation of the line of best fit for bivariate data. The least squares '
                'regression line minimises the sum of the squared vertical distances from each data point to the line. '
                'The equation takes the form y equals a plus bx, where b is the gradient and a is the y-intercept, and '
                'is used to predict the value of y for a given x.',
        'topic': 'statistics'},
    {   'grade': '11',
        'subject': 'mathematics',
        'text': 'The standard normal distribution has a mean of 0 and a standard deviation of 1. Any normal '
                'distribution can be converted to the standard normal by computing a z-score, which equals the value '
                'minus the mean, divided by the standard deviation. Z-scores allow us to find probabilities by looking '
                'up areas under the standard normal curve in a table.',
        'topic': 'statistics'},
    {   'grade': '7',
        'subject': 'mathematics',
        'text': 'Interior angles of a polygon sum to 180 times open bracket n minus 2 close bracket degrees, where n '
                'is the number of sides. For a hexagon with 6 sides, the sum of interior angles is 180 times 4 equals '
                '720 degrees. Each interior angle of a regular hexagon is 720 divided by 6 equals 120 degrees.',
        'topic': 'geometry'},
    {   'grade': '7',
        'subject': 'mathematics',
        'text': 'The exterior angle of a triangle equals the sum of the two non-adjacent interior angles. For example, '
                'if two interior angles of a triangle are 45 degrees and 70 degrees, the exterior angle at the third '
                'vertex is 45 plus 70 equals 115 degrees. The sum of all exterior angles of any convex polygon is '
                'always 360 degrees.',
        'topic': 'geometry'},
    {   'grade': '10',
        'subject': 'mathematics',
        'text': 'Vectors describe a movement in terms of direction and distance. A vector from point A to point B is '
                'written with an arrow above AB or in column form with horizontal and vertical components. Adding '
                'vectors means combining their components: open bracket 3, 2 close bracket plus open bracket 1, '
                'negative 4 close bracket equals open bracket 4, negative 2 close bracket.',
        'topic': 'geometry'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'A tangent to a circle is a straight line that touches the circle at exactly one point, called the '
                'point of tangency. The angle between a tangent and the radius drawn to the point of tangency is '
                'always 90 degrees. Two tangents drawn from an external point to a circle are equal in length.',
        'topic': 'geometry'},
    {   'grade': '10',
        'subject': 'mathematics',
        'text': 'When shapes are enlarged with a scale factor k, areas scale by a factor of k squared and volumes '
                'scale by a factor of k cubed. If two similar solids have a length ratio of 1 to 3, their surface '
                'areas are in the ratio 1 to 9 and their volumes are in the ratio 1 to 27. This is crucial in '
                'engineering and modelling when scaling between prototypes and real objects.',
        'topic': 'geometry'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'A locus is the set of all points that satisfy a given condition. The locus of points equidistant from '
                'a fixed point is a circle. The locus of points equidistant from two fixed points is the perpendicular '
                'bisector of the line segment joining those two points. Loci problems often require combining two or '
                'more conditions.',
        'topic': 'geometry'},
    {   'grade': '8',
        'subject': 'mathematics',
        'text': 'The gradient of a straight line on a coordinate grid is rise divided by run, which equals the change '
                'in y divided by the change in x. For two points with coordinates 1, 3 and 4, 9, the gradient is 9 '
                'minus 3 divided by 4 minus 1 equals 6 over 3 equals 2. The equation of the line through these points '
                'is y equals 2x plus 1.',
        'topic': 'geometry'},
    {   'grade': '8',
        'subject': 'mathematics',
        'text': 'Bearings are angles measured clockwise from North, always written as three figures. A bearing of 045 '
                'degrees means 45 degrees clockwise from North, which is northeast. Bearings are used in navigation '
                'and trigonometry problems involving distances and directions.',
        'topic': 'geometry'},
    {   'grade': '7',
        'subject': 'mathematics',
        'text': 'Relative frequency is used to estimate probability from experimental data. If a drawing pin lands '
                'point up 63 times out of 100 throws, the relative frequency is 0.63. As the number of trials '
                'increases, the relative frequency becomes a more reliable estimate of the true theoretical '
                'probability.',
        'topic': 'probability'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'The addition rule for probability states that P of A or B equals P of A plus P of B minus P of A and '
                'B. The subtraction of P of A and B avoids double-counting the outcomes in the overlap. If two events '
                'are mutually exclusive, P of A and B equals 0, so the rule simplifies to P of A plus P of B.',
        'topic': 'probability'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'When drawing items without replacement, the total number of outcomes decreases with each draw, making '
                'successive events dependent. For example, if a bag contains 5 red and 3 blue counters, the '
                'probability of drawing red then blue is 5 over 8 times 3 over 7 equals 15 over 56. Tree diagrams '
                'clearly display how probabilities change after each draw.',
        'topic': 'probability'},
    {   'grade': '10',
        'subject': 'mathematics',
        'text': 'The multiplication rule for independent events states that P of A and B equals P of A times P of B. '
                'Two events are independent when knowing the outcome of one gives no information about the other. A '
                'simple check: if P of A given B equals P of A, the events are independent.',
        'topic': 'probability'},
    {   'grade': '11',
        'subject': 'mathematics',
        'text': "Bayes' theorem allows us to update the probability of an event based on new evidence. It states that "
                'P of A given B equals P of B given A times P of A, divided by P of B. For example, if a medical test '
                'is 95 percent accurate and 1 percent of the population has a disease, a positive test result does not '
                "mean the patient definitely has the disease; Bayes' theorem shows the actual probability may still be "
                'relatively low.',
        'topic': 'probability'},
    {   'grade': '11',
        'subject': 'mathematics',
        'text': 'The geometric distribution models the number of trials needed to achieve the first success in a '
                'sequence of independent Bernoulli trials. The probability of the first success occurring on the nth '
                'trial is open bracket 1 minus p close bracket to the power n minus 1 times p, where p is the '
                'probability of success. The expected number of trials until the first success is 1 divided by p.',
        'topic': 'probability'},
    {   'grade': '11',
        'subject': 'mathematics',
        'text': 'The Poisson distribution models the number of events occurring in a fixed interval of time or space '
                'when events happen independently at a constant average rate. If the average number of events is '
                'lambda, the probability of exactly k events is e to the power negative lambda times lambda to the '
                'power k, divided by k factorial. It is commonly used to model arrivals, such as customers entering a '
                'shop or calls received per hour.',
        'topic': 'probability'},
    {   'grade': '12',
        'subject': 'mathematics',
        'text': 'The quotient rule is used to differentiate a function that is one expression divided by another. If y '
                'equals u divided by v, then the derivative equals v times the derivative of u minus u times the '
                'derivative of v, all divided by v squared. For example, to differentiate y equals x squared divided '
                'by open bracket x plus 1 close bracket, the derivative is open bracket open bracket x plus 1 close '
                'bracket times 2x minus x squared times 1 close bracket divided by open bracket x plus 1 close bracket '
                'squared, which simplifies to x squared plus 2x divided by open bracket x plus 1 close bracket '
                'squared.',
        'topic': 'calculus'},
    {   'grade': '12',
        'subject': 'mathematics',
        'text': 'The derivative of the natural exponential function e to the power x is itself, e to the power x. The '
                'derivative of the natural logarithm ln of x is 1 divided by x, for x greater than 0. These results, '
                'combined with the chain rule, allow differentiation of expressions like e to the power 3x squared, '
                'whose derivative is 6x times e to the power 3x squared.',
        'topic': 'calculus'},
    {   'grade': '12',
        'subject': 'mathematics',
        'text': 'The trapezium rule is a numerical method for estimating the area under a curve. The area is '
                'approximated by dividing it into trapezoids of equal width h and summing their areas using the '
                'formula: half times h times open bracket y zero plus 2 times open bracket y one plus y two plus dot '
                'dot dot plus y n minus 1 close bracket plus y n close bracket. The more strips used, the closer the '
                'estimate is to the true integral.',
        'topic': 'calculus'},
    {   'grade': '12',
        'subject': 'mathematics',
        'text': 'Integration can be used to find the area between two curves. If f of x is above g of x in the '
                'interval from a to b, the area between them is the integral from a to b of open bracket f of x minus '
                'g of x close bracket dx. First find the x values where the curves intersect by solving f of x equals '
                'g of x, as these form the limits of integration.',
        'topic': 'calculus'},
    {   'grade': '12',
        'subject': 'mathematics',
        'text': 'Implicit differentiation is used when y cannot be easily expressed as a function of x alone. '
                'Differentiate both sides of the equation with respect to x, applying the chain rule to any terms '
                'involving y by multiplying by dy by dx. For the circle equation x squared plus y squared equals 25, '
                'differentiating gives 2x plus 2y times dy by dx equals 0, so dy by dx equals negative x divided by y.',
        'topic': 'calculus'},
    {   'grade': '12',
        'subject': 'mathematics',
        'text': 'Kinematics uses calculus to connect displacement, velocity, and acceleration. Velocity is the '
                'derivative of displacement with respect to time, and acceleration is the derivative of velocity with '
                'respect to time. Conversely, displacement is the integral of velocity and velocity is the integral of '
                "acceleration. If a particle's velocity is v equals 4t minus t squared metres per second, its "
                'displacement after 3 seconds is the integral from 0 to 3 of open bracket 4t minus t squared close '
                'bracket dt, which equals 18 minus 9 equals 9 metres.',
        'topic': 'calculus'},
    {   'grade': '6',
        'subject': 'mathematics',
        'text': 'The Sieve of Eratosthenes is an ancient method for finding all prime numbers up to a given limit. '
                'Start by writing all numbers from 2 upward, then cross out all multiples of 2 greater than 2, then '
                'all multiples of 3 greater than 3, and so on. The numbers that remain are prime. For example, '
                'applying the sieve up to 30 reveals the primes 2, 3, 5, 7, 11, 13, 17, 19, 23, and 29.',
        'topic': 'number theory'},
    {   'grade': '6',
        'subject': 'mathematics',
        'text': 'Divisibility rules are shortcuts to check whether a number is divisible by small integers without '
                'performing full division. A number is divisible by 2 if its last digit is even, by 3 if its digit sum '
                'is divisible by 3, by 5 if it ends in 0 or 5, and by 9 if its digit sum is divisible by 9. For '
                'example, 324 has a digit sum of 9, so it is divisible by both 3 and 9.',
        'topic': 'number theory'},
    {   'grade': '7',
        'subject': 'mathematics',
        'text': 'The HCF and LCM of two numbers can be found efficiently using their prime factorisations. The HCF is '
                'the product of the prime factors common to both numbers, each taken to the lowest power. The LCM is '
                'the product of all prime factors from either number, each taken to the highest power. For 12 equals 2 '
                'squared times 3 and 18 equals 2 times 3 squared, the HCF is 2 times 3 equals 6 and the LCM is 2 '
                'squared times 3 squared equals 36.',
        'topic': 'number theory'},
    {   'grade': '8',
        'subject': 'mathematics',
        'text': 'Recurring decimals are rational numbers whose decimal expansion repeats indefinitely. The fraction '
                'one third equals 0.333 recurring, and one seventh equals 0.142857 recurring. To convert a recurring '
                'decimal to a fraction, let x equal the decimal, multiply by a suitable power of 10 to shift the '
                'recurring block, subtract the original equation, and solve for x.',
        'topic': 'number theory'},
    {   'grade': '8',
        'subject': 'mathematics',
        'text': 'The index law for a power of zero states that any non-zero number raised to the power 0 equals 1. '
                'This follows from the subtraction rule: a to the power n divided by a to the power n equals a to the '
                'power n minus n equals a to the power 0, and any number divided by itself equals 1. Zero to the power '
                'zero is considered indeterminate in most mathematical contexts.',
        'topic': 'number theory'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': "Euclid's algorithm is an efficient method for finding the HCF of two numbers by repeated division. "
                'Divide the larger number by the smaller, note the remainder, then replace the larger number with the '
                'smaller and the smaller with the remainder, repeating until the remainder is zero. For HCF of 252 and '
                '105: 252 equals 2 times 105 plus 42; 105 equals 2 times 42 plus 21; 42 equals 2 times 21 plus 0; so '
                'HCF equals 21.',
        'topic': 'number theory'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'Modular arithmetic deals with remainders after division. We say a is congruent to b modulo n if a and '
                'b have the same remainder when divided by n. For example, 17 is congruent to 2 modulo 5 because both '
                'leave a remainder of 2 when divided by 5. Modular arithmetic is used in cryptography, calendar '
                'calculations, and computer science.',
        'topic': 'number theory'},
    {   'grade': '9',
        'subject': 'mathematics',
        'text': 'An arithmetic series is the sum of the terms of an arithmetic sequence. The sum of the first n terms '
                'is S equals n divided by 2 times open bracket first term plus last term close bracket, or '
                'equivalently S equals n divided by 2 times open bracket 2a plus open bracket n minus 1 close bracket '
                'times d close bracket. For the series 1 plus 3 plus 5 plus dot dot dot plus 99, n equals 50, a equals '
                '1, and l equals 99, giving S equals 50 divided by 2 times 100 equals 2500.',
        'topic': 'number theory'}]
