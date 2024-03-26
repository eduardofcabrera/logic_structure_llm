

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b a)
(on c e)
(on d b)
(on e d)
(clear c)
)
(:goal
(and
(on a d)
(on b e)
(on e c))
)
)


