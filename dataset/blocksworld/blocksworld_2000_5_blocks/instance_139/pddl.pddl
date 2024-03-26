

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a b)
(on b e)
(ontable c)
(on d a)
(on e c)
(clear d)
)
(:goal
(and
(on b a)
(on e d))
)
)


