

(define (problem BW-rand-4)
(:domain blocksworld-4ops)
(:objects a b c d )
(:init
(handempty)
(on a b)
(on b d)
(on c a)
(ontable d)
(clear c)
)
(:goal
(and
(on a c)
(on b a))
)
)

