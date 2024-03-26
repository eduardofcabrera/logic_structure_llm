

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(ontable b)
(on c d)
(on d b)
(on e c)
(clear a)
(clear e)
)
(:goal
(and
(on a b)
(on b e)
(on d c))
)
)


