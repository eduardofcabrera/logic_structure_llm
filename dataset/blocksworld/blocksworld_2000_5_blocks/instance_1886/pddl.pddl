

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b e)
(on c a)
(ontable d)
(on e c)
(clear b)
(clear d)
)
(:goal
(and
(on a d)
(on b c))
)
)


