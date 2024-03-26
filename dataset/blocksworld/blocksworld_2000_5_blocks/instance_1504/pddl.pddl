

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a d)
(ontable b)
(on c e)
(on d c)
(ontable e)
(clear a)
(clear b)
)
(:goal
(and
(on a e)
(on d b)
(on e c))
)
)


