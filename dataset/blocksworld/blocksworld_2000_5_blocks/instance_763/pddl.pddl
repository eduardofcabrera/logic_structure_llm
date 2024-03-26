

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a c)
(ontable b)
(ontable c)
(on d e)
(ontable e)
(clear a)
(clear b)
(clear d)
)
(:goal
(and
(on a b)
(on d c)
(on e a))
)
)


